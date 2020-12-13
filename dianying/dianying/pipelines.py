# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class DianyingPipeline():

    # 如果是将常用变量写在setting中得话，也可以使用下面方法传参

    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self,spider):
        # 链接数据库
        self.db_client = pymongo.MongoClient(self.mongo_uri)
        # 指定到scrapy这个数据库
        self_db = self.db_client[self.mongo_db]
        # 指定集合
        self.collection = self_db['dianying']

    def process_item(self, item, spider):
        # 将item转换为字典
        item_dict = dict(item)
        print(item_dict)
        # 将字典格式的数据插入到集合
        self.collection.insert(item_dict)

    def close_spider(self,spider):
        # 断开数据库链接
        self.db_client.close()
