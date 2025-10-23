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
        self.target_url = 'https://www.binance.com/en/square/news/market-news'

        self.use_selenium_not_requests = True 

    def selenium_actions_on_webpage(self) -> None:
        # remove cookie banner
        self._selenium_driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
        time.sleep(1)
        # only important
        self._selenium_driver.find_element(By.CLASS_NAME, 'bn-switch').click()
        time.sleep(2.5)

    def extract_article_urls(self, soup: BeautifulSoup) -> List[str]:
        news_blocks = soup.find_all('h3', class_='css-ifogq4', recursive=True)
        hrefs = [b.parent['href'] for b in news_blocks]
        a = map(lambda x: urljoin(self.base_url, x), hrefs)
        a = list(set(a))
        dead_end_link = "https://www.binance.com/en/square/post/null"
        if dead_end_link in a:
            a.remove(dead_end_link)
        return a

    def get_title(self, soup: BeautifulSoup) -> str:
        time.sleep(2)
        return soup.find('div', class_="title", recursive=True).get_text()
    
    def get_author(self, soup:BeautifulSoup) -> str:
        t = soup.find_all('a', class_='nick')[0].get_text()
        return t if ' -' not in t else t.split(' -')[0]

    def get_date_published(self, soup:BeautifulSoup) -> str:
        #pub_date = soup.find('div', class_='date').get_text()
        #if pub_date[:4].isnumeric():
        #    # 2023-08-16 13:48
        #    return self.standardize_datetime(pub_date, "%Y-%m-%d %H:%M")
        #else: 
        #    # 16-06-2023 12:50
        #    return self.standardize_datetime(pub_date, "%d-%m-%Y %H:%M")
        date_mm_dd_yyyy = self.current_url.split('post/')[1][:10]
        return self.standardize_datetime(date_mm_dd_yyyy, '%m-%d-%Y')


    def get_text(self, soup: BeautifulSoup) -> str:
        text = soup.find('div', class_='article-body')
        return text.get_text()
