from flask import Blueprint, request, jsonify
from PIL import Image
import os
import io
from model.milvus.milvus_ops import insert_image, delete_image, search_image
from model.data_process.image_process import *
from model.data_process.csv_data_process import save_image_2_csv
from model.common.config import global_config
from model.common.log import logger
from model.common.utils import get_imgs_id_max, set_imgs_id_max
from model.translate import tx_translate

bp = Blueprint('main', __name__)

@bp.route("/image_upload", methods=["POST"])
def image_upload():
    if "image" not in request.files:
        return jsonify({"error": "No image part"}), 400

    file = request.files["image"]
    logger.debug("start upload image <{}>".format(file.filename))
    if file.filename == "":
        return jsonify({"error": "No selected image"}), 400

    if not check_image_suffix(file.filename):
        return jsonify({"error": "Invalid image suffix"}), 400

    try:
        file_data = file.read()
        file_io_data = io.BytesIO(file_data)
        image = Image.open(file_io_data)
    except IOError:
        return jsonify({"error": "Invalid image file"}), 400

    if check_bit_depth(image):
        return jsonify({"error": "32-bit images are not supported"}), 400

    if check_resolution(image):
        return jsonify({"error": "72dpi resolution is not supported"}), 400

    file_path = os.path.join("meme", file.filename)
    repeat_flag, image_md5 = check_image_repeat(image.tobytes())
    if repeat_flag:
        return jsonify({"error": "Image already exists"}), 400

    image_id = get_imgs_id_max() + 1
    set_imgs_id_max(image_id)
    
    save_image(image, file_path)
    insert_image(image_id, file_path)
    
    logger.debug("save image <{}> to csv file <{}>, md5: {}".format(file_path, global_config.csv_file_path, image_md5))
    save_image_2_csv(image_id, image_md5, file_path, global_config.csv_file_path)

    return jsonify({"message": "Image uploaded successfully"})


@bp.route("/image_delete", methods=["POST"])
def image_delete():
    image_ids = request.get_json().get("image_id")
    if not image_ids:
        return jsonify({"error": "Image ID is required"}), 400

    # 调用函数删除图片
    # logger.debug("start delete image <{}>, type: {}".format(image_ids, type(image_ids)))
    res = delete_image(image_ids)

    return jsonify({"message": "Image deleted successfully: {}".format(res)})


@bp.route("/image_search", methods=["POST"])
def image_search():
    text = request.get_json().get("text")
    if not text:
        return jsonify({"error": "text is required"}), 400

    # 判断是否含有中文字符，是的话调用翻译接口
    if any('\u4e00' <= char <= '\u9fff' for char in text):
        text = tx_translate(text)
        
    # 调用函数进行搜索
    img_ids = search_image(text)
    img_paths = get_image_paths(img_ids)

    return jsonify({"results": img_paths})