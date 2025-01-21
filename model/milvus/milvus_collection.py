from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from ..common.log import logger
from ..common.config import global_config


def create_milvus_collection(collection_name, dim):
    logger.info("start init milvus collection <{}>".format(collection_name))
    
    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)
        
    # 设定字段/列: id, embedding
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, descrition="ids", is_primary=True, auto_id=False),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, descrition="embedding vectors", dim=dim)
    ]
    schema = CollectionSchema(fields=fields, description="text image search")
    collection = Collection(name=collection_name, schema=schema)

    # 对embedding建立索引
    # create IVF_FLAT index for collection.
    index_params = {
        "metric_type":"L2",
        "index_type":"IVF_FLAT",
        "params":{"nlist":512}
    }
    collection.create_index(field_name="embedding", index_params=index_params)
    logger.info("milvus collection <{}> init success".format(collection_name))
    return collection

# 连接milvus服务，其中的ip地址为milvus服务所在地址
connections.connect(host=global_config.milvus_server_host, port=global_config.milvus_server_port)

collection = None

# utility.drop_collection(global_config.milvus_collection_name)
# 如果collection不存在就创建
if not utility.has_collection(global_config.milvus_collection_name):
    collection = create_milvus_collection(global_config.milvus_collection_name, global_config.milvus_embedding_dim)
else:
    collection = Collection(name=global_config.milvus_collection_name)
    
logger.debug(f"collection's schema is {collection.schema}, count is {collection.num_entities}")