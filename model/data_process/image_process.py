from ..common.log import logger
from ..common.utils import get_imgs_map, get_imgs_id_map, get_image_md5_from_bytes

# 定义读取图像的函数，根据图像id从csv文件中获取其对应路径再读取
def get_image_paths(images_id):
    logger.debug("get image path from csv file, image_id is {}".format(images_id))
    img_paths = []
    for image_id in images_id[0]:
        path = get_imgs_id_map().get(image_id, "")
        img_paths.append(path)
    return img_paths

def check_image_repeat(image_data):
    md5 = get_image_md5_from_bytes(image_data)
    if md5 in get_imgs_map():
        return True, md5
    return False, md5

# 检查图片后缀是否合法
def check_image_suffix(filename):
    valid_suffixes = {"png", "jpg", "jpeg"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in valid_suffixes

# 检查图片位深度是否为32
def check_bit_depth(image):
    return image.mode == "RGBA" and image.info.get("bitdepth") == 32

# 检查图片分辨率是否为72dpi
def check_resolution(image):
    return image.info.get("dpi") == (72, 72)

# 保存图片到本地
def save_image(image, file_path):
    try:
        image.save(file_path)
    except Exception as e:
        logger.error(f"Failed to save image: {e}")
