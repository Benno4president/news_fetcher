from .scraping_interface import IScraper
import time
import datetime
from typing import List
from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


class CoinTelegraph(IScraper):
    def __init__(self) -> None:
        self.name = 'CoinTelegraph'# must
        self.target_url = 'https://cointelegraph.com/tags/markets' # must
        self.base_url = 'https://cointelegraph.com' # used in extract_article_urls

    def selenium_actions_on_webpage(self) -> None:
        # remove cookie banner
        #self.driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
        time.sleep(1)

    def extract_article_urls(self, soup: BeautifulSoup) -> List[str]:
        news_blocks = soup.find_all('li', class_='posts-listing__item', recursive=True)
        hrefs = [b.find('a', recursive=True)['href'] for b in news_blocks]
        a = map(lambda x: urljoin(self.base_url, x), hrefs)
        return list(set(a))

    def get_title(self, soup: BeautifulSoup) -> str:
        return soup.find('h1', class_='post__title').get_text().strip()
    
    def get_author(self, soup:BeautifulSoup) -> str:
        return soup.find('div', class_='post-meta__author-name').get_text().strip()

    def get_date_published(self, soup:BeautifulSoup) -> str:
        datestr = soup.find('div', class_='post-meta__publish-date').get_text()
        if 'ago' in datestr:
            return self.standardize_datetime(str(datetime.datetime.now().date()), '%Y-%m-%d')
        return self.standardize_datetime(datestr, ' %b %d, %Y ') # fx APR 24, 2023

    def get_text(self, soup: BeautifulSoup) -> str:
        text = soup.find('div', class_='post-content')
        return text.get_text().strip().replace('\n',' ')
