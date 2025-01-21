import argparse
from model.common.config import global_config
from model.common.log import logger
from model.data_process.csv_data_process import csv_generate, csv_init_load
from model.milvus.milvus_ops import load_csv_2_milvus
from model.milvus.milvus_collection import collection
from controller import create_app


def service_init():
    # get collection, if not exists, create
    logger.info("start service init")
    # generate meme id&path csv from folder
    csv_generate(global_config.images_folder, global_config.csv_file_path)
    if collection.num_entities == 0:
        # load meme into milvus databases
        load_csv_2_milvus(global_config.csv_file_path)
    csv_init_load(global_config.csv_file_path)
    logger.info("service init success")
    
def service_start_info(app_host, app_port):
    print("* Running on http://{}:{}/ (Press CTRL+C to quit)".format(app_host, app_port))
    
def service_start(app_host, app_port):
    logger.info("start service")
    
    csv_init_load(global_config.csv_file_path)
    service_start_info(app_host, app_port)
    app = create_app()
    app.run(host=app_host, port=app_port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This is a meme searching service")
    parser.add_argument("-c", "--command", choices=["init", "start"], help="要执行的命令 (init 或 start)")
    input_args = parser.parse_args()
    if input_args.command == "init":
        service_init()
    elif input_args.command == "start":
        service_start(global_config.app_host, global_config.app_port)
        