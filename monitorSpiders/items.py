# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItems(scrapy.Item):
    author = scrapy.Field()
    author_url = scrapy.Field()
    article = scrapy.Field()
    article_create_time = scrapy.Field()
    article_from = scrapy.Field()
    affected_count = scrapy.Field()

    
class MonitorspidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    href = scrapy.Field()
