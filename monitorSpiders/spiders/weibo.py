# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
import re
import time
from ..items import WeiboItems
from urllib.parse import unquote


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


# 获取点赞、评论、转发数
def get_count(common_str):
    if not isinstance(common_str, str):
        count = 0
        return count
    digit_str = re.sub(r"\D", "", common_str)
    if not digit_str:
        count = 0
    else:
        count = int(digit_str)
    return count


# 获取关键字
def get_keyword(url):
    temp = url.split("/")[-1]
    keyword = unquote(temp.split("&")[0])
    return keyword


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.com']
    start_urls = ['https://s.weibo.com']
    keywords = ["逮虾户", "大庆"]

    def start_requests(self):
        for keyword in self.keywords:
            yield Request(url=self.start_urls[0] + "/weibo/" + keyword, callback=self.parse)

    def parse(self, response):
        selector = Selector(response)
        page_list = selector.css(".m-page .s-scroll li")
        for page in page_list:
            url = self.start_urls[0] + page.css("a::attr(href)").extract_first()
            yield Request(url=url, callback=self.handle_data)

    def handle_data(self, response):
        selector = Selector(response)
        card_wrap_list = selector.css(".card-wrap")
        for card_wrap in card_wrap_list:
            content = card_wrap.css(".content")
            if not content.extract_first():
                continue
            keyword = get_keyword(response.request.url) + " "
            author = content.css(".name::text").extract_first()
            author_url = content.css(".name::attr(href)").extract_first()
            article = content.css(".txt").extract_first()
            create_info = content.css(".from")
            create_time = get_time(create_info.xpath("./a[1]/text()").extract_first())
            forwarding = get_count(card_wrap.xpath(".//div[@class='card-act']//li[2]/a/text()").extract_first())
            comments = get_count(card_wrap.xpath(".//div[@class='card-act']//li[3]/a/text()").extract_first())
            stars = get_count(card_wrap.xpath(".//div[@class='card-act']//li[4]/a/em/text()").extract_first())
            # 如何统计受影响人数？简单的将转发、评论、点赞相加吗？我觉得不行，应该将这3者以一定的算法求和，然后相加。
            # 评论的人有极大的可能重复，还有可能对当前微博持反对意见，故取comments * 0.5
            # 点赞和转发的人有3种可能：
            # 1.光点赞不转发
            # 2.光转发不点赞
            # 3.既转发又点赞
            # 故取点赞与转发的最大值+它们的差
            affected_count = comments // 2 + abs(stars - forwarding) + max(stars, forwarding)
            yield WeiboItems(
                keyword=keyword,
                author=author,
                author_url=author_url,
                article=article,
                article_create_time=create_time,
                affected_count=affected_count
            )
