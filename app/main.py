import sys, os
import pandas as pd
from scrapers import active_scrapers
from datahandler import SentimentDBInterface, create_db
from loguru import logger


def parse_args(args):
    """ import argparse """
    if '--init' in args:
        create_db()


def main():
    """
    """
    args = parse_args(sys.argv[1:])
    
    for scraper_name in active_scrapers:
        scraper = active_scrapers[scraper_name]()
        # get id hashes from db (scraper_name)
        ids_from_db = SentimentDBInterface().get_last_hashes(scraper_name, amount=999)

        articles = scraper.run(ignore_ids=ids_from_db)
        articles['origin'] = scraper_name
        
        articles = articles[['hash', 'origin', 'title', 'author', 'published', 'url', 'text']]

        # update state file
        # **

        # save to db
        logger.info('finished scraping {} | new entries: {} | inserting into db...', scraper_name, len(articles))
        SentimentDBInterface().insert_result_dataframe(articles)

    # sleep until repeat
    

if __name__ == '__main__':
    main()