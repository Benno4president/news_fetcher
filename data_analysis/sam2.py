import re
import nltk
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


nltk.download('stopwords') # stopwords punkt
nltk.download('punkt') # stopwords punkt wordnet
nltk.download('wordnet') # stopwords punkt wordnet omw-1.4
nltk.download('omw-1.4') # stopwords punkt wordnet omw-1.4


def sentiment_analysis_m2(text:str) -> pd.DataFrame:
    lemma = WordNetLemmatizer()
    stop_words = stopwords.words('english')
    df = pd.DataFrame()
    def text_prep(x: str) -> list:
         corp = str(x).lower() 
         corp = re.sub('[^a-zA-Z]+',' ', corp).strip() 
         tokens = word_tokenize(corp)
         words = [t for t in tokens if t not in stop_words]
         lemmatize = [lemma.lemmatize(w) for w in words]
         return lemmatize
    preprocess_tag = text_prep(text)
    df["preprocess_txt"] = [preprocess_tag]

    file = open('data_analysis/negative-words.txt', 'r', encoding='iso-8859-1')
    neg_words = file.read().split()
    file = open('data_analysis/positive-words.txt', 'r', encoding='iso-8859-1')
    pos_words = file.read().split()

    num_pos = df['preprocess_txt'].map(lambda x: len([i for i in x if i in pos_words]))
    df['pos_count'] = num_pos
    num_neg = df['preprocess_txt'].map(lambda x: len([i for i in x if i in neg_words]))
    df['neg_count'] = num_neg
    df['sentiment_m2'] = round(df['pos_count'] / (df['neg_count']+1), 2)
    return df

