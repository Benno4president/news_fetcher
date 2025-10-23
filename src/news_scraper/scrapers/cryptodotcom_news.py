from .scraping_interface import IScraper
import time
import datetime
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
        self.use_selenium_not_requests = False  
    
    def selenium_actions_on_webpage(self) -> None:
        # remove cookie banner
        #self.driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
        #time.sleep(1)
        pass

    def extract_article_urls(self, soup: BeautifulSoup) -> List[str]:
        news_blocks = soup.find_all('div', class_='mb-[32px] flex', recursive=True)
        hrefs = [b.find('a', recursive=True)['href'] for b in news_blocks]
        a = map(lambda x: urljoin(self.base_url, x), hrefs)
        return list(set(a))

    def get_title(self, soup: BeautifulSoup) -> str:
        return soup.find('h1', class_='').get_text()
    
    def get_author(self, soup:BeautifulSoup) -> str:
        return 'Research and Insights Team' # no special devisions.

    def get_date_published(self, soup:BeautifulSoup) -> str:
        block = soup.find('div', class_='custom-html-meta-data flex items-center')
        datestr = block.find('span').get_text()
        if len(datestr) in [10, 11]:
            if len(datestr) == 10:
                datestr = '0' + datestr
            return self.standardize_datetime(datestr, '%d %b %Y')
        elif 'HR' in datestr:
            return self.standardize_datetime(str(datetime.date.today()), '%Y-%m-%d')
        elif 'D' in datestr:
            days = datestr.split('D')[0]
            target = str(datetime.date.today() - datetime.timedelta(days=int(days)))
            return self.standardize_datetime(target, '%Y-%m-%d')
        else:
            raise Exception(f'The date is fucked up. Bad parse. datestr: {datestr}')

    def get_text(self, soup: BeautifulSoup) -> str:
        text = soup.find('div', class_='custom-html undefined')
        return text.get_text()
