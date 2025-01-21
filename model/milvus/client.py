from pymilvus import MilvusClient
from ..common.config import global_config

client = MilvusClient(
    uri=f"http://{global_config.milvus_server_host}:{global_config.milvus_server_port}",
)
