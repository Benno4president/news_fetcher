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
        news_blocks = soup.find_all('div', class_='css-1i9bvdl', recursive=True)
        hrefs = [b.find('a', recursive=True)['href'] for b in news_blocks]
        a = map(lambda x: urljoin(self.base_url, x), hrefs)
        return list(set(a))

    def get_title(self, soup: BeautifulSoup) -> str:
        return soup.find('h1', class_='css-ps28d1').get_text()
    
    def get_author(self, soup:BeautifulSoup) -> str: # TODO this is bugged
        t = soup.find_all('div', class_='css-vurnku')[9].get_text()
        return t if ' -' not in t else t.split(' -')[0]

    def get_date_published(self, soup:BeautifulSoup) -> str:
        return soup.find('div', class_='css-1hmgk20').get_text()

    def get_text(self, soup: BeautifulSoup) -> str:
        text = soup.find('article', class_='css-14bbu9p')
        if text is None:
            print('OTHER ARTICLE CSS CLASS FOUND')
            text = soup.find('article', class_='css-17l2a77')
        return text.get_text()

if __name__ == '__main__':
    a = BinanceNews()
    news = a.run()
    print(news)