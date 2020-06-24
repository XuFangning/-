# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector
from scrapy import Request
from movie_review.items import MovieReviewItem
import urllib.request
import re
import json
import csv

'''
  使用Scrapy抓取1000部豆瓣电影id
'''

class DouBanSpider(scrapy.Spider):
    name = 'douban_scrapy'
    allowed_domains = ["douban.com"]
    start_list = []
    for i in range(0,25):
        #url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=' + str(i*20)
        url='https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%AC%A7%E7%BE%8E&sort=time&page_limit=20&page_start=' + str(i*20)
        start_list.append(url)
    for i in range(0,25):
        url='https://movie.douban.com/j/search_subjects?type=movie&tag=%E5%8D%8E%E8%AF%AD&sort=time&page_limit=20&page_start=' + str(i*20)
        start_list.append(url)
    start_urls = start_list   # 定义start_urls为一个存储链接的列表

    def start_requests(self):
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        headers = {'User-Agent': user_agent}
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=headers, method='GET', callback=self.parse)

    def parse(self, response):
        hxs = response.body.decode('utf-8')
        hjson = json.loads(hxs)    # 字典
        for lis in hjson['subjects']:
            item = MovieReviewItem()       # 实例化类
            item["filmid"] = lis['id']
            with open('./data/film_1000.txt', 'a+') as f:
                f.write(item["filmid"])
                f.write('\n')
            print(item["filmid"])
            # filename = item["title"] +item["filmid"]+ '_' + item["score"] + '分' + '.jpg'
            # urllib.request.urlretrieve(item["pic"], filename)
            yield item

