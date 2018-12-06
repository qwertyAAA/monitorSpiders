# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .spidersORM import DBSession, Author, Article, Source


class WeiboPipeline(object):
    def __init__(self):
        self.session = DBSession()

    def process_item(self, item, spider):
        if spider.name == "weibo":
            author = Author(item["author"], item["author_url"])
            source = Source(item["article_from"])
            self.session.add_all([author, source])
            self.session.commit()
            article = Article(
                title=item["article"],
                content=item["article"],
                url="",
                author_id=author.id,
                create_time=item["article_create_time"],
                # 此处的状态（是否危险）如何判断?
                status=0,
                source_id=source.id,
                affected_count=item["affected_count"]
            )
            self.session.add(article)
            self.session.commit()

    def close_spider(self, spider):
        self.session.close()
