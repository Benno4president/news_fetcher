
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0,'.')
from loguru import logger
import argparse

def VALIDATE(expr:bool, msg:str):
        """ EXIT() if false """
        if not expr:
            logger.error(msg)
            exit(1)

def parse_args():
    desc = """
            Hello there!, here you can quick fix a csv to be nicer.
        """
    parser = argparse.ArgumentParser(prog='quick fix',description=desc, usage='idk')
    parser.add_argument('filename', nargs='?')
    return parser.parse_args()

args = parse_args()
fp = Path(args.filename)
VALIDATE(fp.exists(), 'first argument is not a file.')
VALIDATE(fp.name.endswith('.csv'), 'not a csv')
df = pd.read_csv(args.filename, encoding = "ISO-8859-1" ,escapechar='\\')

# hash,author,url,published,origin,title,text,finbert_score,neg,neu,pos,compound,index,preprocess_txt,pos_count,neg_count,sentiment_m2
df = df.drop('index', axis=1)
new_order = ['finbert_score','neg','neu','pos','compound','pos_count','neg_count','sentiment_m2','published','title','origin','hash','author','url','text','preprocess_txt']
df = df[new_order]

df.to_csv(f'{fp.stem}_reordered.csv', index=None, encoding="ISO-8859-1")
