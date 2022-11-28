import os.path as op
import time
import hashlib
from typing import List, Tuple
from urllib.parse import urljoin
from abc import ABC, abstractmethod
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
from loguru import logger
#sudo apt install chromium-chromedriver

#DIR = op.dirname(op.abspath(__file__))


class IScraper(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self.name = ''
        self.base_url = '' # https://www.binance.com
        self.target_url = '' # https://www.binance.com/en/news/top
    
    def run(self, ignore_ids:List[str]=[]) -> pd.DataFrame:
        columns=['hash','url','title','author','published','text']
        article_urls = self.__selenium_get_article_urls()
        new_article_urls = [a for a in article_urls if self.__sha256(a) not in ignore_ids]
        logger.info('{} | New articles found: {}', self.name, len(new_article_urls))

        article_df = pd.DataFrame(columns=columns)
        for article in new_article_urls:
            logger.info('Getting: {}', article)
            res = requests.get(article)
            soup = BeautifulSoup(res.content, 'html.parser')
            row_tuple = self.__scrape_articles(soup)

            uid = self.__sha256(article) # sha256 hash of url #overkill
            row_df = pd.DataFrame([[uid,article,*row_tuple]], columns=columns)
            article_df = pd.concat([article_df, row_df], ignore_index=True)
            time.sleep(2)
        return article_df

    @staticmethod
    def __sha256(text):
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def __scrape_articles(self, soup:BeautifulSoup) -> Tuple[str,str,str,str]:
        title = self.get_title(soup)
        author = self.get_author(soup)
        published = self.get_date_published(soup)
        text = self.get_text(soup)
        return tuple((title, author, published, text))


    def __selenium_get_article_urls(self):
        logger.info('starting selenium driver. ~6s')
        self.driver = self.__get_selenium()
        self.driver.get(self.target_url)
        time.sleep(5)
        self.selenium_actions_on_webpage()
        time.sleep(1) 
        html_doc = self.driver.page_source
        self.driver.close()
        logger.debug('closing selenium driver')
        soup = BeautifulSoup(html_doc, 'html.parser')
        return self.extract_article_urls(soup)
        

    def __get_selenium(self):                           
        """ Creation of driver object """
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('headless')                        
        driver = webdriver.Chrome(options=options)
        return (driver)


    def execute_scrolling(self):
        t0, t1 = 0, 110 # t1 = amount of scrolls
        lastHeight = self.driver.execute_script("return document.documentElement.scrollHeight")
        print('Start height:', lastHeight)

        while True:
            for i in range(1,10):
                self.driver.execute_script(f"window.scrollTo(0, {lastHeight*(i*0.1)});")
                #driver.execute_script("window.scrollBy(0, 250)")
                #driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                time.sleep(0.2)
            time.sleep(0.8)    
            newHeight = self.driver.execute_script("return document.documentElement.scrollHeight")
            print('t =',t0,'/',t1,'|','newHeight', newHeight)

            if newHeight == lastHeight or t0 >= t1:
                break
            lastHeight = newHeight
            t0 += 1


    @abstractmethod
    def selenium_actions_on_webpage(self) -> None:
        """ Use self.driver to interact with the selenium driver """
        raise NotImplementedError
    
    @abstractmethod
    def extract_article_urls(self, soup: BeautifulSoup) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_title(self, soup:BeautifulSoup) -> str:
        """ 
        input: soup containing entire article.
        return: title of the article, not the webpage.
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_author(self, soup:BeautifulSoup) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_date_published(self, soup:BeautifulSoup) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def get_text(self, soup:BeautifulSoup) -> str:
        raise NotImplementedError


