import pymongo


class MongoDBWriter:
    def __init__(self, host, port, database, collection_name):
        self.client = pymongo.MongoClient(host, port)  # 输入mongodb的url以及post
        self.db = self.client[database]
        self.collection = self.db[collection_name]

    def write_item(self, item):
        # 将item的字段名作为表头，值作为数据
        data = {key: value for key, value in item.items()}
        self.collection.insert_one(data)


def save_item(spider_name, item):
    # 根据spider_name创建数据库集合名称
    collection_name = f"result_{spider_name}"

    # 创建MongoDBWriter实例，输入mongodb的url、post以及database
    mongo_writer = MongoDBWriter(host="your_mongodb_host", port=27017, database="your_database_name",
                                 collection_name=collection_name)

    # 写入item到MongoDB
    mongo_writer.write_item(item)


"""
        save_item(spider.name, result)#调用save_item时，需要多传递一个spider.name参数
"""
