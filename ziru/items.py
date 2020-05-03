# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZiruItem(scrapy.Item):
    # define the fields for your item here like:
    return_code = scrapy.Field()
    message = scrapy.Field()
    data = scrapy.Field()


class CommunityItem(scrapy.Item):
    code = scrapy.Field()
    count = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    building_state = scrapy.Field()
    sell_price = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    distance = scrapy.Field()
    duration = scrapy.Field()
    icon = scrapy.Field()


