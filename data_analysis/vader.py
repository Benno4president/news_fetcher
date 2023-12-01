from typing import Any
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon') # stopwords punkt wordnet omw-1.4 vader_lexicon


def sentiment_analysis_vader(text:str) -> pd.DataFrame:
    sent = SentimentIntensityAnalyzer()
    return pd.DataFrame.from_dict([sent.polarity_scores(text)])

class Vader:
    """ Calling this returns the vader compound score """
    def __init__(self) -> None:
        self.analyzer = SentimentIntensityAnalyzer()
    def __call__(self, text):
        return self.analyzer.polarity_scores(text)
