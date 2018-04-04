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
    start_urls = [
        BASE_URL.format('1')
    ]
    page = 1

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
        coin_item['coin'] = response.xpath('//h1/img/@alt').extract_first()
        coin_item['short_name'] = response.xpath("//h1/img/following-sibling::small[@class='bold hidden-xs']/text()").extract_first().strip('()')
        coin_item['rank'] = response.xpath("//span[@class='label label-success']/text()").extract_first().replace('Rank ', '')
        coin_item['website'] = '\n'.join(response.xpath("//ul/li/span[@title='Website']/following-sibling::a/@href").extract())
        coin_item['price_usd'] = response.xpath("//span[@id='quote_price']/span[@class='text-large2']/text()").extract_first()
        coin_item['price_btc'] = response.xpath("//span[contains(.,'BTC')]/span/text()").extract_first().replace('\n', '')
        coin_item['change_24_usd'] = response.xpath("//span[@class='text-large2  negative_change']/span/text()").extract_first()
        coin_item['market_cap_usd'] = response.xpath("//span[@data-currency-market-cap]/@data-usd").extract_first()
        coin_item['volume_24_usd'] = response.xpath("//span[@data-currency-volume]/@data-usd").extract_first()


        yield coin_item