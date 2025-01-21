# milvus_meme_search
A meme search service based on Milvus. 

基于Milvus的表情包检索服务



## 如何使用

1. 搭建milvus服务：

   ```bash
   curl -sfL https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh -o standalone_embed.sh
   
   bash standalone_embed.sh start
   ```

2. 配置config.json（若使用中文作为输入，需申请[腾讯翻译api](https://links.jianshu.com/go?to=https%3A%2F%2Fcloud.tencent.com%2Fdocument%2Fproduct%2F551%2F35017)）

3. 复制您的表情包图片到meme文件夹中

4. 初始化服务：

   ```bash
   python3 ./main.py -c init
   ```

5. 启动服务：

   ```bash
   python3 ./main.py -c start
   ```

   
