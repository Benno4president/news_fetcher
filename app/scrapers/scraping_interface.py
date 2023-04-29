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
import datetime
#sudo apt install chromium-chromedriver


class IScraper(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self.name:str = ''
        self.base_url:str = '' # https://www.binance.com
        self.target_url:str = '' # https://www.binance.com/en/news/top
    
    def run(self, ignore_ids:List[str]=[], display_head=False) -> pd.DataFrame:
        self.display_head = display_head
        columns=['hash','url','title','author','published','text']
        article_urls = self.__selenium_get_article_urls()
        new_article_urls = [a for a in article_urls if self.__sha256(a) not in ignore_ids]
        logger.info('{} | New articles found: {}', self.name, len(new_article_urls))

        article_df = pd.DataFrame(columns=columns)
        for article in new_article_urls:
            logger.info('Getting: {}', article)
            res = requests.get(article, headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0'})
            logger.debug('Page content size: {}', len(res.content))
            soup = BeautifulSoup(res.content, 'html.parser')
            row_tuple = self.__scrape_articles(soup)

            uid = self.__sha256(article) # sha256 hash of url #overkill
            row_df = pd.DataFrame([[uid,article,*row_tuple]], columns=columns)
            article_df = pd.concat([article_df, row_df], ignore_index=True)
            time.sleep(2)
        return article_df

    @staticmethod
    def standardize_datetime(timestr:str, in_format:str) -> str:
        """
        Used to convert a datetime string to a consistent format.
        Docs: https://docs.python.org/2/library/datetime.html?highlight=strftime#strftime-and-strptime-behavior
        """
        return str(datetime.datetime.strptime(timestr, in_format).strftime('%Y-%m-%d %H:%M'))
    
    @staticmethod
    def __sha256(text):
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def __scrape_articles(self, soup:BeautifulSoup) -> Tuple[str,str,str,str]:
        title = self.get_title(soup)
        logger.debug('Title: {}', title)
        author = self.get_author(soup)
        logger.debug('Author: {}', author)
        published = self.get_date_published(soup)
        logger.debug('Pub: {}', published)
        text = self.get_text(soup)
        logger.debug('Text len: {}', len(text))
        return tuple((title, author, published, text))


    def __selenium_get_article_urls(self):
        logger.info('starting selenium driver. ~6s')
        self.driver = self.__get_selenium()
        self.driver.get(self.target_url)
        time.sleep(5)
        self.selenium_actions_on_webpage()
        if self.display_head:
            time.sleep(45)
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
        if not self.display_head:
            options.add_argument('headless')                        
        driver = webdriver.Chrome(options=options)
        return (driver)


    def execute_scrolling(self):
        """ Not done, from old project """
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
        """
        Use self.driver to interact with the active selenium driver
        to remove banners, scroll etc.. 
        whatevers needs to be done in the browser.
        """
        raise NotImplementedError
    
    @abstractmethod
    def extract_article_urls(self, soup: BeautifulSoup) -> List[str]:
        """ 
        The soup param is the parsed html of the self.target_url.
        This must return the list of urls containing the articles on the site.
        """
        raise NotImplementedError

    @abstractmethod
    def get_title(self, soup:BeautifulSoup) -> str:
        """ return the title of the article, not the webpage, as a string. """
        raise NotImplementedError
    
    @abstractmethod
    def get_author(self, soup:BeautifulSoup) -> str:
        """ return the author of the article as a string."""
        raise NotImplementedError

    @abstractmethod
    def get_date_published(self, soup:BeautifulSoup) -> str:
        """ return the publish date of the article as a string in the format 'yyyy-mm-dd hh:mm'. """
        raise NotImplementedError
    
    @abstractmethod
    def get_text(self, soup:BeautifulSoup) -> str:
        """ return the text of the article as a single string. """
        raise NotImplementedError


