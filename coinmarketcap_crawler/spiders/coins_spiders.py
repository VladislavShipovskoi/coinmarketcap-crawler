import scrapy
from scrapy.spiders import CrawlSpider
from coinmarketcap_crawler.items import CoinmarketcapItem

BASE_URL = 'https://coinmarketcap.com/{}'


class CoinmarketcapSpider(CrawlSpider):
    name = "coinmarketcapspider"
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'coins.csv'
    }

    def __init__(self, page=1,min_price=0,max_price=float("inf"),*args, **kwargs):
        super(CoinmarketcapSpider, self).__init__(*args, **kwargs)
        self.page = int(page)
        self.min_price = float(min_price)
        self.max_price = float(max_price)
        self.start_urls = [BASE_URL.format(page)]

    def parse(self, response):
        all_url = response.xpath("//tbody/tr/td/span/a/@href").extract()
        if all_url:
            for url in all_url:
                yield scrapy.Request(
                    response.urljoin(url),
                    callback=self.parse_coin
                )
            self.page += 1

            yield scrapy.Request(
                BASE_URL.format(self.page),
                callback=self.parse
            )

    def parse_coin(self,response):
        coin_item = CoinmarketcapItem()
        try:
            price = float(response.xpath("//span[@id='quote_price']/span[@class='text-large2']/text()").extract_first().replace(',', '.'))
        except ValueError:
            price = None
        if price and (self.min_price < price < self.max_price):
            coin_item['price_usd'] = price
            coin_item['coin'] = response.xpath('//h1/img/@alt').extract_first()
            coin_item['short_name'] = response.xpath("//h1/img/following-sibling::small[@class='bold hidden-xs']/text()").extract_first().strip('()')
            coin_item['rank'] = response.xpath("//span[@class='label label-success']/text()").extract_first().replace('Rank ', '')
            coin_item['website'] = '\n'.join(response.xpath("//ul/li/span[@title='Website']/following-sibling::a/@href").extract())
            coin_item['price_btc'] = response.xpath("//span[contains(.,'BTC')]/span/text()").extract_first().replace('\n', '')
            coin_item['change_24_usd'] = response.xpath("//span[contains(@class, '_change')]/span[@data-format-value]/text()").extract_first()
            coin_item['market_cap_usd'] = response.xpath("//span[@data-currency-market-cap]/@data-usd").extract_first()
            coin_item['volume_24_usd'] = response.xpath("//span[@data-currency-volume]/@data-usd").extract_first()
            yield coin_item
