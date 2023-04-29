from .binance_news import BinanceNews
from .cryptodotcom_news import CryptoDotCom
from .cointelegraph_news import CoinTelegraph

active_scrapers = {
    'binance_news': BinanceNews,
    'crypto_news': CryptoDotCom,
    'coin_telegraph':CoinTelegraph
}