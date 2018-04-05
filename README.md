# coinmarketcap-crawler

This is web crawler coinmarketcap data.Results are contained in the csv file.

## Start
1. make virtualenv and run
```bash
python3 -m venv /path/to/new/virtual/environment
source /path/to/new/virtual/environment/bin/activate
```

2. install packages:
```bash
pip install -r requirements.txt
```
3. run spider:
```bash
scrapy crawl coinmarketcapspider
```
## Arguments
* page - the start page (default page = 1)
```bash
scrapy crawl coinmarketcapspider -a page=2
```
* min_price - min price coin in USD (will be collected all the coins whose price is greater min_price,default=0)
```bash
scrapy crawl coinmarketcapspider -a min_price=10
```
* max_price - max price coin in USD (will collect all coins, the price of which is less than max_price,default=infinity)
```bash
scrapy crawl coinmarketcapspider -a max_price=20
```
* Arguments can be used either individually or together
```bash
scrapy crawl coinmarketcapspider -a min_price=10 -a max_price=20 -a page=2
```

## Data
Spider collect:
* coin name,abbreviation,website,rank
* coin price in USD,BTC
* coin price change(24h) in %
* coin volume(24h) in usd
* coin market cap in usd

![1](https://user-images.githubusercontent.com/17500704/38324092-7794b058-3869-11e8-9ee1-10c4812df282.png)
