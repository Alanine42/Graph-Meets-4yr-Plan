# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import sys
from scrapy.exporters import JsonLinesItemExporter
from .items import CourseItem

class LocalPipeline:
    def open_spider(self, spider):
        self.file = open('courseObjects.json', 'ab+')   # append in binary, +read
        self.exporter = JsonLinesItemExporter(self.file)
        self.exporter.start_exporting()
        
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        

class MongoDBPipeline:
    
    collection = 'scrapy_items'   # can change!!   'course_index'
    
    def __init__(self, mongodb_uri, mongodb_db):
        self.mongodb_uri = mongodb_uri
        self.mongodb_db = mongodb_db
        if not self.mongodb_uri:
            sys.exit("You need to provide a Connection String.")
            
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_uri=crawler.settings.get('MONGODB_URI'),
            mongodb_db=crawler.settings.get('MONGODB_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        # Start with a clean database
        self.db[self.collection].delete_many({})
        
    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        data = dict(CourseItem(item))
        self.db[self.collection].insert_one(data)
        return item
    