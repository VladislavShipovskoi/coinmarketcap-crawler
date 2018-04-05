import scrapy
from scrapy.spiders import CrawlSpider
from coinmarketcap_crawler.items import AllCoinsData

BASE_URL = 'https://coinmarketcap.com/{}'


class AllCoinsSpider(CrawlSpider):
    name = "all-coins"

    def __init__(self, page=1, min_price=0, max_price=float("inf"), *args,**kwargs):
        super(AllCoinsSpider, self).__init__(*args, **kwargs)
        self.page = int(page)
        self.min_price = min_price
        self.max_price = max_price
        self.start_urls = [BASE_URL.format(self.page)]

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

    def parse_coin(self, response):
        coin_item = AllCoinsData()
        price = response.xpath(
            "//span/span[@class='text-large2']/text()"
        ).extract_first()
        if not price:
            return
        try:
            price = float(price.replace(',', '.'))
        except ValueError:
            return
        if price and (self.min_price < price < self.max_price):
            coin_item['price_usd'] = price
            coin_item['name'] = response.xpath("//h1/img/@alt").extract_first()
            coin_item['type'] = response.xpath(
                "//span[@class='label label-warning'][1]/text()"
            ).extract_first()
            coin_item['short_name'] = response.xpath(
                "//h1/small[@class='bold hidden-xs']/text()"
            ).extract_first().strip('()')
            coin_item['rank'] = response.xpath(
                "//span[@class='label label-success']/text()"
            ).extract_first().replace('Rank ', '')
            coin_item['website'] = '\n'.join(
                response.xpath(
                    "//ul/li/span[@title='Website']/following-sibling::a/@href"
                ).extract())
            coin_item['price_btc'] = response.xpath(
                "//span[contains(.,'BTC')]/span/text()"
            ).extract_first().replace('\n', '')
            coin_item['change_24'] = response.xpath(
                "//span[contains(@class, '_change')]/span/@data-format-value"
            ).extract_first()
            coin_item['market_cap_usd'] = response.xpath(
                "//span[@data-currency-market-cap]/@data-usd"
            ).extract_first()
            coin_item['volume_24_usd'] = response.xpath(
                "//span[@data-currency-volume]/@data-usd"
            ).extract_first().replace('?', '')
            yield coin_item
