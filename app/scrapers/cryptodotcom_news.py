from .scraping_interface import IScraper
import time
from typing import List
from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


class CryptoDotCom(IScraper):
    def __init__(self) -> None:
        self.name = 'CryptoDotCom'# must
        self.target_url = 'https://crypto.com/market-updates' # must
        self.base_url = 'https://crypto.com' # used in extract_article_urls

    def selenium_actions_on_webpage(self) -> None:
        # remove cookie banner
        #self.driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
        time.sleep(1)

    def extract_article_urls(self, soup: BeautifulSoup) -> List[str]:
        news_blocks = soup.find_all('div', class_='card-container underline normal-list-card', recursive=True)
        hrefs = [b.find('a', recursive=True)['href'] for b in news_blocks]
        a = map(lambda x: urljoin(self.base_url, x), hrefs)
        return list(set(a))

    def get_title(self, soup: BeautifulSoup) -> str:
        return soup.find('h1', class_='article-title').get_text()
    
    def get_author(self, soup:BeautifulSoup) -> str:
        return 'Research and Insights Team' # no special devisions.

    def get_date_published(self, soup:BeautifulSoup) -> str:
        datestr = soup.find('span', class_='article-university-details-date').get_text()
        return self.normalize_datetime(datestr, '%b %d, %Y')

    def get_text(self, soup: BeautifulSoup) -> str:
        text = soup.find('div', class_='article-box-text')
        return text.get_text()
