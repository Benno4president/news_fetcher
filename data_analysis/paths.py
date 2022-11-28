import os
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
__model_dir = os.path.join(BASE_PATH,'model')
if not os.path.exists(__model_dir):
    os.mkdir(__model_dir)

TOKENIZER_PATH = os.path.join(__model_dir,'FBERT.tokenizer')
MODEL_PATH = os.path.join(__model_dir, 'FBERT.model')