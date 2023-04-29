from .binance_news import BinanceNews
from .cryptodotcom_news import CryptoDotCom

active_scrapers = {
    'binance_news': BinanceNews,
    'crypto_news': CryptoDotCom
}