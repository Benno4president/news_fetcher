import sys
import argparse
from loguru import logger
import pandas as pd
from scrapers import active_scrapers
from datahandler import SentimentDBInterface, create_db

def parse_args():
    desc = """
            Hello there!, welcome to a low code news article fetcher.
            Start scraping any news source using only very litte and 
            very googlable python code.
        """
    parser = argparse.ArgumentParser(prog='News Fetcher',description=desc, usage='just press play')
    parser.add_argument('-t', '--test', action='store_true', help="Won't save to db, but prints instead")
    parser.add_argument('-s', '--scraper', choices=['all']+list(active_scrapers.keys()), 
                        default='all', help='Specify a single scraper to run')
    parser.add_argument('--init', action='store_true', help="Populate the database, then run.")
    parser.add_argument('-i','--interactive', action='store_true', help="Manually control selenium for an extended time.")
    return parser.parse_args()
    

def run_scrape(args):
    db = SentimentDBInterface()
    for scraper_name in active_scrapers:
        try:
            scraper = active_scrapers[scraper_name]()
            # get id hashes from db (scraper_name)
            ids_from_db = db.get_last_hashes(scraper_name, amount=9999)

            articles: pd.DataFrame = scraper.run(ignore_ids=ids_from_db, display_head=args.interactive)
            articles['origin'] = scraper_name

            articles = articles[['hash', 'origin', 'title', 'author', 'published', 'url', 'text']]

            # update state file
            # **

            # save to db
            if args.test:
                print('Labels:')
                print(articles.columns)
                print('-'*45)
                print(articles)
                articles.to_csv(f'./newsfetcher_debug_{scraper_name}.csv')
            else:
                logger.info('finished scraping {} | new entries: {} | inserting into db...', scraper_name, len(articles))
                db.insert_result_dataframe(articles)
        except Exception as e:
            logger.error('{} thrown on {}', e, scraper_name)


def main():
    """
    """
    global active_scrapers # yes, i mutate a global, embrace chaos.
    args = parse_args()
    print(args)
    
    # Remove to reset logging level to something else
    logger_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<level>{message}</level>"
    )
    logger.remove(0)
    logger.add(sys.stderr, format=logger_format, level="INFO" if not args.test else "DEBUG")

    if args.init:
        create_db()
    if args.scraper != 'all':
        active_scrapers = {args.scraper:active_scrapers.pop(args.scraper)}
    
    #:repeat
    run_scrape(args)
    # sleep
    

if __name__ == '__main__':
    main()