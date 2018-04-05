# -*- coding: utf-8 -*-

from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter


class CoinmarketcapCrawlerPipeline(object):

    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('%s.csv' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        if spider.name == "all-coins":
            self.exporter.fields_to_export = [
                'rank',
                'coin',
                'short_name',
                'website',
                'market_cap_usd',
                'price_usd',
                'price_btc',
                'volume_24_usd',
                'change_24',
            ]
        elif spider.name == "historical-data":
            self.exporter.fields_to_export = [
                'date',
                'open_price',
                'high_price',
                'low_price',
                'close_price',
                'volume',
                'market_cap',
            ]
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
