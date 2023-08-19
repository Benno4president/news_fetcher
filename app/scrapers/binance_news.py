from .scraping_interface import IScraper
import time
from typing import List
from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


class BinanceNews(IScraper):
    def __init__(self) -> None:
        self.name = 'Binance'
        self.base_url = 'https://www.binance.com'
        self.target_url = 'https://www.binance.com/en/news/top'

    def selenium_actions_on_webpage(self) -> None:
        # remove cookie banner
        self.driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
        time.sleep(1)

    def extract_article_urls(self, soup: BeautifulSoup) -> List[str]:
        news_blocks = soup.find_all('div', class_='css-2eyo4q', recursive=True)
        hrefs = [b.find('a', recursive=True)['href'] for b in news_blocks]
        a = map(lambda x: urljoin(self.base_url, x), hrefs)
        a = list(set(a))
        dead_end_link = "https://www.binance.com/en/feed/post/null"
        if dead_end_link in a:
            a.remove(dead_end_link)
        return a

    def get_title(self, soup: BeautifulSoup) -> str:
        return soup.find('h1', class_='title').get_text()
    
    def get_author(self, soup:BeautifulSoup) -> str:
        t = soup.find_all('a', class_='css-1vx7e2')[0].get_text()
        return t if ' -' not in t else t.split(' -')[0]

    def get_date_published(self, soup:BeautifulSoup) -> str:
        pub_date = soup.find('div', class_='date').get_text()
        if pub_date[:4].isnumeric():
            # 2023-08-16 13:48
            return self.standardize_datetime(pub_date, "%Y-%m-%d %H:%M")
        else: 
            # 16-06-2023 12:50
            return self.standardize_datetime(pub_date, "%d-%m-%Y %H:%M")

    def get_text(self, soup: BeautifulSoup) -> str:
        text = soup.find('div', class_='article-body')
        return text.get_text()
