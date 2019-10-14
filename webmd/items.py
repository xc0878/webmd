# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WebmdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    supplement = scrapy.Field()
    conditionInfo = scrapy.Field()
    dateTime = scrapy.Field()
    reviewerInfo = scrapy.Field()
    effectiveness = scrapy.Field()
    easeOfUse = scrapy.Field()
    satisfaction = scrapy.Field()
    comment = scrapy.Field()
    helpful = scrapy.Field()
