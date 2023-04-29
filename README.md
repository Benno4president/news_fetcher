# News Monitor
This repo contains:
- A news source scraper app.
- A data analysis 'lib' containing a set of text sentiment methods.
- A set of tools to pull and transform stored data.

## Installation
```bash
# get repository.
git clone git@github.com:Benno4president/news_fetcher.git
# create a virtual environment (optional).
python3 -m venv venv
# install the required libs.
pip3 install -r requirements.txt
# install the driver needed by selenium.
sudo apt install chromium-chromedriver
```
### Database
```bash
# if there is no database.db file,
# this is needed to initialize a new one.
python3 app/main.py --init
```

## Usage
```bash
# scraper usage.
python3 app/main.py --help 
# create a csv of sentiment values.
python3 tools/db2coin_sentiment.py 
# to build a .gexf file.
python3 tools/build_graph.py 
```
## Add scraper interface
First, create a new Scraper Interface python file in the scrapers directory:
```py
from .scraping_interface import IScraper

class BinanceNews(IScraper):
    def __init__(self) -> None:
        # must be set
        self.name = 'Binance'
        self.target_url = 'https://www.binance.com/en/news/top'
        # any needed instance values can be set, if needed
        self.base_url = 'https://www.binance.com'

```
Apart from init, IScraper contains 6 abstract methods to overwrite.
```py
    def selenium_actions_on_webpage(self) -> None:
        """
        Use self.driver to interact with the active selenium driver
        to remove banners, scroll etc.. 
        whatevers needs to be done in the browser.
        """
    
    def extract_article_urls(self, soup: BeautifulSoup) -> List[str]:
        """ 
        The soup param is the parsed html of the self.target_url.
        This must return the list of urls containing the articles on the site.
        """

    def get_title(self, soup:BeautifulSoup) -> str:
        """ return the title of the article, not the webpage, as a string. """
    
    def get_author(self, soup:BeautifulSoup) -> str:
        """ return the author of the article as a string."""

    def get_date_published(self, soup:BeautifulSoup) -> str:
        """ return the publish date of the article as a string in the format 'yyyy-mm-dd hh:mm'. """
    
    def get_text(self, soup:BeautifulSoup) -> str:
        """ return the text of the article as a single string. """
```
When you are ready to test, add the class to the active_scrapers in __init__ to make it visible.
```py
from .binance_news import BinanceNews
from .your_new_scraper import NewsSource

active_scrapers = {
    'binance_news': BinanceNews,
    'name_of_your_scraper': NewsSource
}
```
The run the test of your new scraper.
```bash
python3 app/main.py --test --scraper name_of_your_scraper
```

## dev notes
use lib:
- https://github.com/dbader/schedule
- https://github.com/Delgan/loguru