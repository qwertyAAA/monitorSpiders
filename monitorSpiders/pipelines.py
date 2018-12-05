# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class MonitorspidersPipeline(object):
#     def process_item(self, item, spider):
#         return item
from monitorSpiders import settings


class FilePipeline(object):
    def __init__(self,path):
        self.f=None
        self.path=path

    @classmethod
    def from_crawler(cls, crawler):
        print("file from_crawler")
        path=crawler.settings.get('FILE_PATH')
        print(path)
        return cls(path)

    def open_spider(self, spider):

        if spider.name=='tieba':
            print('file open_spider')
            self.f=open(self.path,'a+',encoding='utf-8')


    def process_item(self, item, spider):
        print('file write')
        self.f.write(item["title"] + '\n')
        self.f.write(item["href"]+'\n')


    def close_spider(self, spider):
        print('File close_spider')
        self.f.close()