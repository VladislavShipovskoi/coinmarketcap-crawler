# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AllCoinsData(scrapy.Item):
    name = scrapy.Field()
    type = scrapy.Field()
    website = scrapy.Field()
    rank = scrapy.Field()
    short_name = scrapy.Field()
    market_cap_usd = scrapy.Field()
    price_usd = scrapy.Field()
    price_btc = scrapy.Field()
    volume_24_usd = scrapy.Field()
    change_24 = scrapy.Field()


class HistoricalData(scrapy.Item):
    date = scrapy.Field()
    open_price = scrapy.Field()
    high_price = scrapy.Field()
    low_price = scrapy.Field()
    close_price = scrapy.Field()
    volume = scrapy.Field()
    market_cap = scrapy.Field()
