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
            author = self.session.query(Author).filter_by(author_url=item["author_url"]).first()
            source = self.session.query(Source).filter_by(source="新浪微博").first()
            if not author:
                author = Author(author=item["author"], author_url=item["author_url"])
                self.add_data(author)
            if not source:
                source = Source(source="新浪微博")
                self.add_data(source)
            article = self.session.query(Article).filter_by(author_id=author.id,
                                                            create_time=item["article_create_time"]).first()
            if not article:
                article = Article(
                    title="",
                    content=item["article"],
                    detail="",
                    url="",
                    author_id=author.id,
                    create_time=item["article_create_time"],
                    # 此处的状态（是否危险）如何判断?
                    status=0,
                    source_id=source.id,
                    affected_count=item["affected_count"],
                    keywords=item["keyword"]
                )
                self.add_data(article)
            else:
                keywords = article.keywords
                if keywords.find(item["keyword"]) == -1:
                    keywords += item["keyword"]
                    article.keywords = keywords
                    self.session.commit()

    def close_spider(self, spider):
        self.session.close()

    def add_data(self, data):
        self.session.add(data)
        self.session.commit()


class FilePipeline(object):
    def __init__(self, path):
        self.f = None
        self.path = path

    @classmethod
    def from_crawler(cls, crawler):
        print("file from_crawler")
        path = crawler.settings.get('FILE_PATH')
        print(path)
        return cls(path)

    def open_spider(self, spider):
        if spider.name == 'tieba':
            print('file open_spider')
            self.f = open(self.path, 'a+', encoding='utf-8')

    def process_item(self, item, spider):
        print('file write')
        self.f.write(item["title"] + '\n')
        self.f.write(item["href"] + '\n')

    def close_spider(self, spider):
        print('File close_spider')
        self.f.close()
