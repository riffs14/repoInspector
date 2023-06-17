#utils.py
import re
import nltk
import os
from github_inspector.config import git_api_url
import json

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

def simple_validation(github_link,open_ai_key,submitted):
    msg=""
    if submitted:
        if len(github_link)<0:
            msg="Enter The Github link"
            return (True,msg)
        if not open_ai_key.startswith('sk-'):
            msg= "Enter a valid Open AI Key"
            return (True,msg)
        else:
            return (False,msg)
    else:
        return(False,msg)



def repo_link_collector(github_profile_link):
    list_repo=[]
    github_link=os.path.join(git_api_url,github_profile_link,'repos')
            
    result = os.popen("curl "+github_link).read()
    try:
        json_object = json.loads(result)

        for count,i in enumerate(json_object):
            if i['visibility']=='public':
                list_repo.append(i['html_url'])
    except:
        return list_repo,""
        #pass
    return list_repo,result