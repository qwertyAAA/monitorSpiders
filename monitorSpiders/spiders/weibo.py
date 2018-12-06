# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
import re
import time
from ..items import WeiboItems


# 将微博的创建时间进行格式化
def get_time(time_str):
    time_str = re.sub(r"\D", " ", time_str)
    time_str = time_str.strip()
    if 5 < len(time_str) <= 12:
        time_str = time.strftime("%Y ") + time_str
        time_str = time.strftime("%Y-%m-%d %H:%M", time.strptime(time_str, "%Y %m %d %H %M"))
    elif 2 < len(time_str) <= 5:
        time_str = time.strftime("%Y-%m-%d ") + time_str.replace(" ", ":")
    elif 0 < len(time_str) <= 2:
        stamp = time.time() - float(time_str) * 60
        time_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(stamp))
    else:
        time_str = time.strftime("%Y-%m-%d %H:%M")
    return time_str


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
        card_wrap_list = selector.css(".card-wrap")
        for card_wrap in card_wrap_list:
            content = card_wrap.css(".content")
            author = content.css(".name::text").extract_first()
            author_url = content.css(".name::attr(href)").extract_first()
            article = content.css(".txt").extract_first()
            article_create_time = content.css(".from a::text").extract()[0].strip()
            article_from = content.css(".from a::text").extract()[1]
            forwarding = card_wrap.xpath(".//div[@class='card-act']//li[2]/text()").extract_first()
            forwarding = int(re.sub(r"\D", "", forwarding))
            comments = card_wrap.xpath(".//div[@class='card-act']//li[3]/text()").extract_first()
            comments = int(re.sub(r"\D", "", comments))
            stars = card_wrap.xpath(".//div[@class='card-act']//li[4]//em/text()").extract_first()
            stars = int(re.sub(r"\D", "", stars))
            # 如何统计受影响人数？简单的将转发、评论、点赞相加吗？我觉得不行，应该将这3者以一定的算法求和，然后相加。
            affected_count = comments // 2 + abs(stars - forwarding) + max(stars, forwarding)
            # 评论的人有极大的可能重复，还有可能对当前微博持反对意见，故取comments * 0.5
            # 点赞和转发的人有3种可能：
            # 1.光点赞不转发
            # 2.光转发不点赞
            # 3.既转发又点赞
            # 故取点赞与转发的最大值+它们的差
            yield WeiboItems(
                author=author,
                author_url=author_url,
                article=article,
                article_create_time=article_create_time,
                article_from=article_from,
                affected_count=affected_count
            )
