# -*- coding: utf-8 -*-
import pymongo

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BloombergPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):

    collection_name = 'bloomberg_articles'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        aid_count = self.db[self.collection_name].find({"article_id":item["article_id"]}).count()
        ### prevent duplicate articles
        if aid_count == 0:
            self.db[self.collection_name].insert_one(dict(item))
        else:
            print('=======================Duplicated aid====================', item["article_id"])
        ###save tags
        #for i in item["tags"]:
        #    self.db.tags.update({"name":i})
        return item
