import logging
import pathlib
from .config import global_config


abs_path = str(pathlib.Path(__file__).parent.parent.absolute())
# 日志设置
logging.basicConfig(filename=f"{abs_path}/{global_config.log_file}", level=logging.DEBUG, format="[%(funcName)s] %(asctime)s - %(levelname)s - %(lineno)d: %(message)s")
logger = logging.getLogger(__name__)
