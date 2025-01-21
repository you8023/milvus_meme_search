import json
import pathlib


class Config:
    def __init__(self, config_name):
        abs_path = str(pathlib.Path(__file__).parent.parent.absolute())
        self.global_config = json.load(open(f"{abs_path}/{config_name}", encoding="utf-8"))
        
        # set default value if the neccesary param is null
        if not self.global_config["app_host"]:
            self.global_config["app_host"] = "0.0.0.0"
        if not self.global_config["app_port"]:
            self.global_config["app_port"] = "5000"
        if not self.global_config["log_file"]:
            self.global_config["log_file"] = "meme_search.log"
        if not self.global_config["milvus_server_host"]:
            self.global_config["milvus_server_host"] = "127.0.0.1"
        if not self.global_config["milvus_server_port"]:
            self.global_config["milvus_server_port"] = "19530"
        if not self.global_config["milvus_collection_name"]:
            self.global_config["milvus_collection_name"] = "meme_search"
        if not self.global_config["model_name"]:
            self.global_config["model_name"] = "clip_vit_base_patch16"
        if not self.global_config["milvus_embedding_dim"]:
            self.global_config["milvus_embedding_dim"] = 512
        if not self.global_config["images_folder"]:
            self.global_config["images_folder"] = "meme"
        if not self.global_config["csv_file_path"]:
            self.global_config["csv_file_path"] = "meme_images.csv"
            

    def __getattr__(self, name):
        if name in self.global_config.keys():
            return self.global_config[name]
        return ""

global_config = Config("../config.json")