import requests
from bs4 import BeautifulSoup


article = "https://www.binance.com/en/square/post/10-14-2025-bitcoin-price-watch-btc-down-to-111-4k-as-etf-outflows-and-macro-tensions-weigh-heavily-30998576351458"

res = requests.get(article, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0'})

soup = BeautifulSoup(res.content)

a = soup.find('div')

print(res.content)