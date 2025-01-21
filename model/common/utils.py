import hashlib
from ..common.log import logger
from PIL import Image

imgs_map = {}
imgs_id_max = 0
imgs_id_map = {}

get_imgs_map = lambda: imgs_map
get_imgs_id_max = lambda: imgs_id_max
get_imgs_id_map = lambda: imgs_id_map

def set_imgs_map(new_imgs_map):
    global imgs_map
    imgs_map = new_imgs_map

def set_imgs_id_max(new_imgs_id_max):
    global imgs_id_max
    imgs_id_max = new_imgs_id_max

def set_imgs_id_map(new_imgs_id_map):
    global imgs_id_map
    imgs_id_map = new_imgs_id_map

def get_image_md5(file_path):
    try:
        image = Image.open(file_path)
        return get_image_md5_from_bytes(image.tobytes())
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    
def get_image_md5_from_bytes(image_bytes):
    md5 = hashlib.md5()
    md5.update(image_bytes)
    return md5.hexdigest()