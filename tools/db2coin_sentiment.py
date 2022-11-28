import sys
import datetime
import pandas as pd
sys.path.insert(0,'.')

from app.datahandler import ToolDBInterface
from data_analysis import build_sentiment_pipeline, test_pipeline, sentiment_analysis_m2, sentiment_analysis_vader


def iter_scraperresults_by_date(db):

    to_date = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M').date()
    raw_dates_in_db = db.get_published_dates()
    dates_in_db = [to_date(d) for d in raw_dates_in_db]

    # iterate over days
    start_date = datetime.date(year=2022, month=6, day=1)
    end_date   = datetime.date(year=2022, month=12, day=1)

    # Iterating over all dates from start date until end date including end date ("inclusive")
    current_date = start_date

    while current_date <= end_date:
        # Calling the function that you need, with the appropriate day-month-year combination
        # Outputting to path that is build based on current day-month-year combination.
        # Advancing current date by one day
        current_date += datetime.timedelta(days=1)
        if not current_date in dates_in_db:
            continue # for now
        dates_to_get = [raw_dates_in_db[i] for i,x in enumerate(dates_in_db) if current_date == x]
        res = db.get_all_by_date(dates_to_get)
        yield res, str(current_date)


df = pd.DataFrame()
db = ToolDBInterface()

nlp = build_sentiment_pipeline()
nlp_key = lambda x: nlp(x[:512])[0]['label']

for srx, datestr in iter_scraperresults_by_date(db):
    for sr in srx:
        new_df = sentiment_analysis_m2(sr.text)
        new_df['id'] = sr.hash
        new_df['date'] = datestr
        new_df['sentiment_model'] = nlp_key(sr.text)
        new_df['preprocess_txt'] = ' '.join(new_df['preprocess_txt'].values[0]) # consistent seperator

        # vader return needs better names
        new_df = pd.concat([new_df, sentiment_analysis_vader(sr.text)], axis=1)
        df = pd.concat([df, new_df])

df.to_csv('tools/db2coin_out.csv', index=None)