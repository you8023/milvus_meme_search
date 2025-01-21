import csv
import os
import pandas as pd
from ..common.log import logger
from ..common.utils import get_image_md5
from ..common.utils import set_imgs_map, set_imgs_id_map, set_imgs_id_max, get_imgs_id_max, get_imgs_map, get_imgs_id_map


def csv_generate(folder_path, save_path):
    logger.info("start init csv file <{}> from <{}>".format(save_path, folder_path))
    index = 0
    with open(save_path, "w", encoding="utf-8", newline="") as f:
        csv_writer = csv.writer(f)
        # 写入csv标题
        csv_writer.writerow(["id", "md5", "path", "label"])
        # 遍历目录，将id和图片路径添加到csv文件中
        for filepath, _, files in os.walk(folder_path):
            for file_name in files:
                file_all_path = os.path.join(filepath, file_name)
                
                # 计算图片md5
                image_md5 = get_image_md5(file_all_path)
                csv_writer.writerow([index, image_md5, file_all_path,""])
                index += 1
    logger.info("csv file <{}> init success".format(save_path))

# 将图片信息保存到csv文件
def save_image_2_csv(image_id, image_md5, image_path, csv_path):
    logger.debug("save image <{}> to csv file <{}>".format(image_path, csv_path))
    with open(csv_path, "a", encoding="utf-8") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([image_id, image_md5, image_path, ""])
    temp_imgs_map = get_imgs_map()
    temp_imgs_map[image_md5] = image_path
    set_imgs_map(temp_imgs_map)
    temp_imgs_id_map = get_imgs_id_map()
    temp_imgs_id_map[image_id] = image_path
    set_imgs_id_map(temp_imgs_id_map)

def csv_init_load(file_path):
    logger.info("start load csv file from <{}>".format(file_path))
    df = pd.read_csv(file_path)
    set_imgs_map(df.set_index("md5")["path"].to_dict())
    set_imgs_id_map(df.set_index("id")["path"].to_dict())
    for the_id in df["id"]:
        if int(the_id) > get_imgs_id_max():
            set_imgs_id_max(int(the_id))
    logger.info("csv file <{}> load success, max_id is {}".format(file_path, get_imgs_id_max()))