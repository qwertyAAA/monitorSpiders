# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrapy.http import Request, cookies
from selenium.webdriver.support.wait import WebDriverWait
from monitorSpiders.items import MonitorspidersItem

class TiebaSpider(scrapy.Spider):
    name = 'tieba'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['http://tieba.baidu.com/']
    key_words=['大庆油田']
    url = []
    def start_requests(self):
        print('开始')
        for key_word in self.key_words:
            urls=['http://tieba.baidu.com/f/search/res?ie=utf-8&qw=']
            # meta = {'proxy': 'http://211.138.61.27'}
            for url in urls:
                yield Request(url=url+key_word,)

    def parse(self, response):
        print('解析')
        print(response)
        brower=webdriver.PhantomJS()
        brower.get(response.url)
        #通过获取尾页url来获取全部url
        # end_href=brower.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[5]/a[11]').get_attribute('href')
        # num=end_href.rindex('=')
        # end_page=end_href[num+1:]
        # print(end_page)
        # page_list = brower.find_elements_by_xpath('/html/body/div[4]/div/div[2]/div[5]/a')
        # for i in range(1,int(end_page)+1):
        #     yield Request(url=end_href[0:num+1]+str(i), callback=self.index)
        #直接获取当前页面下的所有分页
        page_list = brower.find_elements_by_xpath('/html/body/div[4]/div/div[2]/div[5]/a')
        for i in page_list:
            if (not i.text in ['首页', '尾页', '下一页>', '<上一页']) and (not i.get_attribute('href') in self.url):
                self.url.append(i.get_attribute('href'))
        print(self.url)
        for i in self.url:
            yield Request(url=i, callback=self.storage)

    def storage(self, response):
        print('存储')
        brower = webdriver.PhantomJS()
        brower.get(response.url)
        list=brower.find_elements_by_xpath('/html/body/div[4]/div/div[2]/div[3]/div[3]/div')
        for i in list:
            ti = i.find_element_by_xpath('.//span/a').text
            hr = i.find_element_by_xpath('.//span/a').get_attribute('href')
            yield MonitorspidersItem(title=ti, href=hr)


