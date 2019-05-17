from pymongo import MongoClient
from scrapy.exceptions import DropItem
from scrapy import log


# -*- coding: utf-8 -*-

class MongoDBPipeline:
    
    def __init__(self):
        client = MongoClient()
        db = client.tcc
        self.collection = db.filmes

    def process_item(self, item):
        self.collection.update({'link': item['link']}, dict(item), upsert=True)
        log.msg(f"Movie '{item['name']}' added to MongoDB database!",
                level=log.DEBUG)
        return item
    