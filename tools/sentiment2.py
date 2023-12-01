import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0,'.')
from loguru import logger
import argparse

def parse_args():
    desc = """
            Hello there!, here you can add some sentiment.
        """
    parser = argparse.ArgumentParser(prog='stick a ',description=desc, usage='idk')
    parser.add_argument('filename', nargs='?')
    parser.add_argument('column_name', nargs='?')
    parser.add_argument('-t', '--test', action='store_true', help="idk")
    return parser.parse_args()

def VALIDATE(expr:bool, msg:str):
        """ EXIT() if false """
        if not expr:
            logger.error(msg)
            exit(1)

if __name__ == '__main__':
    args = parse_args()
    logger.debug(args)
    # fix.. some day..
    from data_analysis import build_sentiment_pipeline, test_pipeline, sentiment_analysis_m2, Vader
    # Remove to reset logging level to something else
    logger_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<level>{message}</level>"
    )
    logger.remove(0)
    logger.add(sys.stderr, format=logger_format, level="INFO" if not args.test else "DEBUG")
    
    
    fp = Path(args.filename)
    logger.debug(fp)
    VALIDATE(fp.exists(), 'first argument is not a file.')
    VALIDATE(fp.name.endswith('.csv'), 'not a csv')

    df = pd.read_csv(args.filename, encoding = "ISO-8859-1" ,escapechar='\\')
    logger.debug(df.columns)
    VALIDATE(args.column_name in df.columns, 'second argument not found in csv.')
    text = df[args.column_name]
    
    nlp = build_sentiment_pipeline() # financial bert
    nlp_key = lambda x: nlp(x[:512])[0]['label'] # 'label' and 'score'
    logger.debug(nlp_key('yolo this is wild.'))
    df['finbert_score'] = text.apply(lambda x: nlp_key(str(x))) # usign str only hides the problem
    del(nlp)

    vader = Vader()
    logger.debug(vader('yolo this is wild.'))
    df = pd.concat([df, pd.DataFrame([vader(str(x)) for x in text])], axis=1)
    logger.debug(df.columns)
    del(vader)

    logger.debug(sentiment_analysis_m2('yolo this is wild.'))
    df = pd.concat([df, pd.concat([sentiment_analysis_m2(str(x)) for x in text], axis=0).reset_index()], axis=1)
    logger.debug(df.columns)

    df.to_csv(f'{fp.stem}_sentiment.csv', index=None, encoding="ISO-8859-1")
