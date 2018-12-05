# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from ..spidersORM import session, Article, Author, Source


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.com']
    start_urls = ['https://s.weibo.com']
    keywords = ["逮虾户"]

    def start_requests(self):
        for keyword in self.keywords:
            yield Request(url=self.start_urls[0] + "/weibo/" + keyword, callback=self.parse)

    def parse(self, response):
        selector = Selector(response)
        # conn = pymysql.connect(host="10.25.116.62", user="root", password="123456", database="monitor")
        # cursor = conn.cursor()
        content_list = selector.css(".content")
        for content in content_list:
            author = content.css(".name::text").extract_first()
            author_url = content.css(".name::attr(href)").extract_first()
            article = content.css(".txt").extract_first()
            article_create_time = content.css(".from a::text").extract()[0]
            article_from = content.css(".from a::text").extract()[1]
            data = session.query(Author).all()
            print(data)
            # sql = """
            #     INSERT INTO `monitor.SpiderDB_author` VALUES(
            #         DEFAULT,
            #         {author},
            #         {author_url}
            #     );
            # """.format(author=author, author_url=author_url)
            # sql += """
            #     INSERT INTO `monitor.SpiderDB_source` VALUES(
            #         DEFAULT,
            #         {article_from}
            #     );
            # """.format(article_from=article_from)
            # sql += """
            #     INSERT INTO `monitor.SpiderDB_`
            # """


