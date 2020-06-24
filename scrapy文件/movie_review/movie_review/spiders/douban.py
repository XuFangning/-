# -*- coding: utf-8 -*-
import re
import csv
import scrapy
from scrapy.http import Request
#建立存评论的文件
 with open('./data/review1000.csv','w') as f:
     csv_write = csv.writer(f)
     csv_head = ["movie","comment_type(1:good,1:bad)","comment_content"]
     csv_write.writerow(csv_head)

class DouBanSpider(scrapy.Spider):
    name = 'douban'
     
    def start_requests(self):
        #打开存有电影id的文件,并将电影id一列表的形式存到film_list
        with open('./data/film_1000.txt', 'r') as f:
            filmid_list = f.readlines()
        for movie_id in filmid_list:
            for start in range(0, 200, 20):
                meta = {
                    'sentiment': 1
                }
                movie_id = movie_id.replace('\n', '')
                #好评网址
                url = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=new_score&status=P&percent_type=h'.format(movie_id, start)
                yield Request(url=url, meta=meta)
                meta = {
                    'sentiment': 0
                }
                movie_id = movie_id.replace('\n', '')
                #差评网址
                url = 'https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=new_score&status=P&percent_type=l'.format(movie_id, start)
                yield Request(url=url, meta=meta)

    def parse(self, response):
         #读评论内容
        review_list = response.xpath('//span[@class="short"]/text()').extract()
         #读是哪个电影的短评
        review_name = "".join(response.xpath('//*[@id="content"]/h1/text()').extract())
        print(review_list)
        for review in review_list:
            review = review.strip()
            review = review.replace('\t', '')
            review = review.replace('\n', '')
            review = review.replace('\xa0', '')
            review = review.replace('\ufeff', '')
            review = review.replace('\u200b', '')

            #写入文件
            if review:
                with open('./data/review1000.csv', 'a+',newline='') as f:
                    csv_write = csv.writer(f)#可以理解为初始化
                    data_row = [review_name,response.meta['sentiment'], review]
                    csv_write.writerow(data_row)
