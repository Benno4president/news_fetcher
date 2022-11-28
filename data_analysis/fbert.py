from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
from .paths import MODEL_PATH, TOKENIZER_PATH
import os

def build_sentiment_pipeline():

    if not (os.path.exists(MODEL_PATH) and os.path.exists(TOKENIZER_PATH)):
        __update_fbert()

    model = BertForSequenceClassification.from_pretrained(MODEL_PATH,num_labels=3)
    tokenizer = BertTokenizer.from_pretrained(TOKENIZER_PATH)
    
    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    return nlp


def test_pipeline(nlp):
    sentences = ["Operating profit rose to EUR 13.1 mn from EUR 8.7 mn in the corresponding period in 2007 representing 7.7 % of net sales.",  
                 "Bids or offers include at least 1,000 shares and the value of the shares must correspond to at least EUR 4,000.", 
                 "Raute reported a loss per share of EUR 0.86 for the first half of 2009 , against EPS of EUR 0.74 in the corresponding period of 2008.", 
                 ]
    results = nlp(sentences)
    print('~~ Sentiment analysis test ~~')
    __import__('pprint').pprint(results)


def __update_fbert():
    """
    https://huggingface.co/ahmedrachid/FinancialBERT-Sentiment-Analysis
    """
    model = BertForSequenceClassification.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis",num_labels=3)
    tokenizer = BertTokenizer.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis")

    tokenizer.save_pretrained(TOKENIZER_PATH)
    model.save_pretrained(MODEL_PATH)


if __name__ == '__main__':
    __update_fbert()
    print("""
    FBERT saved.
    Download model using hugging face lib.
    https://huggingface.co/docs/transformers/installation
    """)
