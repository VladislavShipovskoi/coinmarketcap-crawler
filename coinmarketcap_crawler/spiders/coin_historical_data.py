import datetime
from scrapy.spiders import CrawlSpider
from coinmarketcap_crawler.items import HistoricalData

BASE_URL = 'https://coinmarketcap.com/currencies/{}/historical-data/?start={}&end={}'


class HistoricalDataSpider(CrawlSpider):

    name = "historical-data"

    def __init__(self, currency='bitcoin',start=None,end=None,*args, **kwargs):
        super(HistoricalDataSpider, self).__init__(*args, **kwargs)
        self.currency = currency
        self.start = start
        if end and start:
            self.end = end
            self.start = start
        else:
            self.end = datetime.datetime.today().strftime('%Y%m%d')
            self.start = '20100101'
        self.start_urls = [BASE_URL.format(self.currency,self.start,self.end)]

    def parse(self, response):
        all_data = response.xpath("//tbody/tr[@class='text-right']")
        if all_data:
            for data in all_data:
                print(data)
                historical_data_item = HistoricalData()
                historical_data_item['date'] = data.xpath("td[1]/text()").extract_first()
                historical_data_item['open_price'] = data.xpath("td[2]/@data-format-value").extract_first()
                historical_data_item['high_price'] = data.xpath("td[3]/@data-format-value").extract_first()
                historical_data_item['low_price'] = data.xpath("td[4]/@data-format-value").extract_first()
                historical_data_item['close_price'] = data.xpath("td[5]/@data-format-value").extract_first()
                historical_data_item['volume'] = data.xpath("td[6]/@data-format-value").extract_first()
                historical_data_item['market_cap'] = data.xpath("td[7]/@data-format-value").extract_first()
                yield historical_data_item
