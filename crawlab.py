import pymongo


class MongoDBWriter:
    def __init__(self, host, port, collection_name, username, password):
        self.client = pymongo.MongoClient(host, port, username=username, password=password)

        self.db = self.client['test']
        self.collection = self.db[collection_name]

    def write_item(self, item):
        data = {key: value for key, value in item.items()}
        self.collection.insert_one(data)


def save_item(spider_name, item):
    collection_name = f"results_{spider_name}"

    username = "userName"
    password = "password"

    mongo_writer = MongoDBWriter(host="127.0.0.1", port=27017,collection_name=collection_name, username=username, password=password)

    mongo_writer.write_item(item)



"""
        save_item(spider.name, result)#调用save_item时，需要多传递一个spider.name参数
"""
