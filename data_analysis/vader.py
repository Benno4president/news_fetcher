import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon') # stopwords punkt wordnet omw-1.4 vader_lexicon


def sentiment_analysis_vader(text:str) -> pd.DataFrame:
    sent = SentimentIntensityAnalyzer()
    return pd.DataFrame.from_dict([sent.polarity_scores(text)])
