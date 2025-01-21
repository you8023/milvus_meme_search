import csv
import os
from towhee import ops, pipe
import numpy as np
from ..common.config import global_config
from .client import client
from .milvus_collection import collection
from ..common.log import logger

p_image_insert = (
    pipe.input("id", "path")
    .map("path", "img", ops.image_decode.cv2("rgb"))
    .map("img", "vec", ops.image_text_embedding.clip(model_name=global_config.model_name, modality="image"))
    .map("vec", "vec", lambda x: x / np.linalg.norm(x))
    .map(("id", "vec"), "result", ops.ann_insert.milvus_client(host=global_config.milvus_server_host, port=global_config.milvus_server_port, collection_name=global_config.milvus_collection_name))
    .output("result")
)


# 定义csv文件的数据处理方式
def read_csv(csv_path, encoding="utf-8-sig"):
    if os.path.exists(csv_path) == False:
        logger.error(f"csv file <{csv_path}> not exists")
    with open(csv_path, "r", encoding=encoding) as f:
        data = csv.DictReader(f)
        for line in data:
            yield int(line["id"]), line["path"]

# 定义数据处理流水线：
# 1. 输入csv文件
# 2. 通过上述定义的read_csv函数处理csv数据，拿到其中的id和path
# 3. 通过ops.image_decode.cv2读取路径中的image图像
# 4. 通过ops.image_text_embedding.clip指定clip_vit_base_patch16作为处理模型，将图像转换为向量数据
# 5. 通过lambda x: x / np.linalg.norm(x)对向量数据进行线性处理
# 6. 通过ops.ann_insert.milvus_client将处理后的向量数据及id存储到milvus数据库中，其中的collection_name参数需和上述建立的collection名称一致
p_csv_load = (
    pipe.input("csv_file")
    .flat_map("csv_file", ("id", "path"), read_csv)
    .map("path", "img", ops.image_decode.cv2("rgb"))
    .map("img", "vec", ops.image_text_embedding.clip(model_name=global_config.model_name, modality="image", device=0))
    .map("vec", "vec", lambda x: x / np.linalg.norm(x))
    .map(("id", "vec"), (), ops.ann_insert.milvus_client(host=global_config.milvus_server_host, port=global_config.milvus_server_port, collection_name=global_config.milvus_collection_name))
    .output()
)

# 定义数据处理流水线：
# 1. 输入text文本
# 2. 通过ops.image_text_embedding.clip指定clip_vit_base_patch16作为模型处理文本，得到向量数据
# 3. 通过lambda x: x / np.linalg.norm(x)将向量数据进行线性转换
# 4. 通过ops.ann_search.milvus_client检索数据库中的相似向量，其中的collection_name参数需和上述建立的collection名称一致
# 5. 对检索结果进行处理，获取图像id
# 6. 通过上述定义的read_image函数，读取图像内容
p_search = (
    pipe.input("text")
    .map("text", "vec", ops.image_text_embedding.clip(model_name=global_config.model_name, modality="text"))
    .map("vec", "vec", lambda x: x / np.linalg.norm(x))
    .map("vec", "result", ops.ann_search.milvus_client(host=global_config.milvus_server_host, port=global_config.milvus_server_port, collection_name=global_config.milvus_collection_name, limit=5))
    .map("result", "image_ids", lambda x: [item[0] for item in x])
    .output("image_ids")
)

def insert_image(image_id, image_path):
    p_image_insert(image_id, image_path)
    collection.load()
    logger.debug("insert image <{}> to milvus success, now entity count is {}".format(image_path, collection.num_entities))

def delete_image(image_ids):
    res = client.delete(collection_name=global_config.milvus_collection_name, ids=image_ids)
    collection.load()
    logger.debug("delete image <{}> from milvus: {}, now entity count is {}".format(image_ids, res, collection.num_entities))
    return res

def load_csv_2_milvus(csv_file):
    logger.info("start load csv file <{}> to milvus".format(csv_file))
    p_csv_load(csv_file)
    collection.load()
    logger.info("load csv file <{}> to milvus success, now count is {}".format(csv_file, collection.num_entities))

def search_image(text):
    return p_search(text).get()