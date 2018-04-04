import scrapy
from scrapy.spiders import CrawlSpider
from coinmarketcap_crawler.items import CoinmarketcapItem

BASE_URL = 'https://coinmarketcap.com/{}'


class CoinmarketcapSpider(CrawlSpider):
    pass