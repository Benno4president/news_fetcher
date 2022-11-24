import sys, os
import datetime
import re
sys.path.insert(0,'./sentiment/')
from datahandler import ToolDBInterface, ScraperResult

import nltk
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer


nltk.download('stopwords') # stopwords punkt
nltk.download('punkt') # stopwords punkt wordnet
nltk.download('wordnet') # stopwords punkt wordnet omw-1.4
nltk.download('omw-1.4') # stopwords punkt wordnet omw-1.4 vader_lexicon
nltk.download('vader_lexicon') # stopwords punkt wordnet omw-1.4 vader_lexicon


def sentiment_analysis_m2(text:str):
    lemma = WordNetLemmatizer()
    stop_words = stopwords.words('english')
    sent = SentimentIntensityAnalyzer()
    df = pd.DataFrame()
    def text_prep(x: str) -> list:
         corp = str(x).lower() 
         corp = re.sub('[^a-zA-Z]+',' ', corp).strip() 
         tokens = word_tokenize(corp)
         words = [t for t in tokens if t not in stop_words]
         lemmatize = [lemma.lemmatize(w) for w in words]
         return lemmatize
    preprocess_tag = text_prep(text) #[text_prep(i) for i in df['text']]
    df["preprocess_txt"] = [preprocess_tag]
    df['sentiment_vader_txt'] = round(sent.polarity_scores(text)['compound'], 2)
    df['sentiment_vader_pp'] = round(sent.polarity_scores(' '.join(preprocess_tag))['compound'], 2)

    file = open('tools/negative-words.txt', 'r', encoding='iso-8859-1')
    neg_words = file.read().split()
    file = open('tools/positive-words.txt', 'r', encoding='iso-8859-1')
    pos_words = file.read().split()

    num_pos = df['preprocess_txt'].map(lambda x: len([i for i in x if i in pos_words]))
    df['pos_count'] = num_pos
    num_neg = df['preprocess_txt'].map(lambda x: len([i for i in x if i in neg_words]))
    df['neg_count'] = num_neg
    df['sentiment_m2'] = round(df['pos_count'] / (df['neg_count']+1), 2)
    return df


def iter_scraperresults_by_date(db):

    to_date = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M').date()
    raw_dates_in_db = db.get_published_dates()
    dates_in_db = [to_date(d) for d in raw_dates_in_db]

    # iterate over days
    start_date = datetime.date(year=2022, month=6, day=1)
    end_date   = datetime.date(year=2022, month=12,  day=1)

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


df = pd.DataFrame(columns=['id','date','preprocess_txt','pos_count','neg_count','sentiment_m2', 'sentiment_model', 'sentiment_vader'])
db = ToolDBInterface()
for srx, datestr in iter_scraperresults_by_date(db):
    for sr in srx:
        new_df = sentiment_analysis_m2(sr.text)
        new_df['id'] = sr.hash
        new_df['date'] = datestr
        new_df['sentiment_model'] = sr.sentiment
        new_df['preprocess_txt'] = ' '.join(new_df['preprocess_txt'].values[0]) # consistent seperator
        df = pd.concat([df, new_df])

df.to_csv('tools/db2coin_out.csv', index=None)