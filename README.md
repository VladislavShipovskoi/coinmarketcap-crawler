# coinmarketcap-crawler

This is web crawler coinmarketcap data.Results are contained in the file coins.csv.

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
## Data
Spider collect:
* coin name,abbreviation,website,rank
* coin price in USD,BTC
* coin price change(24h) in usd
* coin volume(24h) in usd
* coin market cap in usd

![1](https://user-images.githubusercontent.com/17500704/38324092-7794b058-3869-11e8-9ee1-10c4812df282.png)
