# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CoinmarketcapItem(scrapy.Item):
    coin = scrapy.Field()
    website = scrapy.Field()
    rank = scrapy.Field()
    # mineable = scrapy.Field()
    # market_cap = scrapy.Field()
    price = scrapy.Field()
    # volume_24 = scrapy.Field()
    # change_24 = scrapy.Field()
