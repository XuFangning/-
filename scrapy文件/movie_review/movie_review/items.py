# -*- coding: utf-8 -*-


import scrapy


class MovieReviewItem(scrapy.Item):
    review = scrapy.Field()
    sentiment = scrapy.Field()
    review_name=scrapy.Field()
    filmid=scrapy.Field()