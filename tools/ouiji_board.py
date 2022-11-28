import sys
from transformers import pipeline

qa_model = pipeline("question-answering")

#context = sys.argv[1]
sys.path.insert(0,'.')
from app.datahandler import ToolDBInterface

context = ToolDBInterface().get_all_text()
context = '. '.join(context[:10])

while True:
    question = input("Ask a question.\n")
    anws = qa_model(question=question, context=context)
    print('Answer: ',anws['answer'],'\nConfidence:', anws['score'])
