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
    short_name = scrapy.Field()
    market_cap_usd = scrapy.Field()
    price_usd = scrapy.Field()
    price_btc = scrapy.Field()
    volume_24_usd = scrapy.Field()
    change_24_usd = scrapy.Field()
