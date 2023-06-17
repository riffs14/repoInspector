#utils.py
import re
import nltk
import os

nltk.download("punkt")

def clean_and_tokenize(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'\b(?:http|ftp)s?://\S+', '', text)
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\d+', '', text)
    text = text.lower()
    # print(nltk.word_tokenize(text))
    # input()
    return nltk.word_tokenize(text)

def format_documents(documents,hardness):
    numbered_docs = "\n".join([f"{i+1}. {os.path.basename(doc.metadata['source'])}: {doc.page_content}" for i, doc in enumerate(documents)])
    numbered_docs_list=[]
    ind=0
    while(ind<len(numbered_docs)):
        numbered_docs_list.append(numbered_docs[ind:ind+4000])
        # print(len(numbered_docs_list))
        # input("iun util file ,")
        ind=ind+5000
    # if len(numbered_docs)>4000:
    #     numbered_docs=numbered_docs[:10]
    return numbered_docs_list[:hardness]

def format_user_question(question):
    question = re.sub(r'\s+', ' ', question).strip()
    return question
