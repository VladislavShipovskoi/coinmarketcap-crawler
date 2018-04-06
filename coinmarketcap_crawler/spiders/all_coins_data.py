import scrapy
from scrapy.spiders import CrawlSpider
from coinmarketcap_crawler.items import AllCoinsData

BASE_URL = 'https://coinmarketcap.com/{}'


class AllCoinsSpider(CrawlSpider):
    name = "all-coins"

    def __init__(self, page=1, min_price=0, max_price=float("inf"), *args,
                 **kwargs):
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
            rank = response.xpath(
                "//span[@class='label label-success']/text()"
            ).extract_first()

            coin_item['name'] = response.xpath(
                "//h1/img/@alt"
            ).extract_first()

            coin_item['type'] = response.xpath(
                "//span[@class='label label-warning'][1]/text()"
            ).extract_first()

            symbol = response.xpath(
                "//h1/small[@class='bold hidden-xs']/text()"
            ).extract_first()

            website = response.xpath(
                "//ul/li/span[@title='Website']/following-sibling::a/@href"
            ).extract()

            market_cap_usd = response.xpath(
                "//span[@data-currency-market-cap]/@data-usd"
            ).extract_first()

            price_btc = response.xpath(
                "//span[contains(.,'BTC')]/span/text()"
            ).extract_first()

            volume_24_usd = response.xpath(
                "//span[@data-currency-volume]/@data-usd"
            ).extract_first()

            change_24 = response.xpath(
                "//span[contains(@class, '_change')]/span/@data-format-value"
            ).extract_first()

            if not change_24:
                change_24 = "unknown"

            if not website:
                website = "unknown"
            else:
                website = '\n'.join(website)

            coin_item['price_usd'] = price
            coin_item['website'] = website
            coin_item['change_24'] = change_24
            coin_item['symbol'] = symbol.strip('()')
            coin_item['rank'] = rank.replace('Rank ', '')
            coin_item['price_btc'] = price_btc.replace('\n', '')
            coin_item['volume_24_usd'] = volume_24_usd.replace('?', 'unknown')
            coin_item['market_cap_usd'] = market_cap_usd.replace(
                'None', 'unknown'
            )

            yield coin_item
