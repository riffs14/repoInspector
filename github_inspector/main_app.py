#main.py
import os
import tempfile
from dotenv import load_dotenv
from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI
from github_inspector.config import WHITE, GREEN, RESET_COLOR, model_name,openai_api_key
from github_inspector.utils import format_user_question
from github_inspector.file_processing import clone_github_repo, load_and_index_files
from github_inspector.questions import ask_question, QuestionContext
import json
from langchain.text_splitter import CharacterTextSplitter
from tqdm import tqdm
from langchain.chains.summarize import load_summarize_chain

load_dotenv()

def run(key):
    openai_api_key=key

    llm = OpenAI(openai_api_key=openai_api_key, temperature=0.2)

    template = """
    Repo: {repo_name} ({github_url}) | Conv: {conversation_history} | Docs: {numbered_documents} | Q: {question} | FileCount: {file_type_counts} | FileNames: {filenames}

    Instr : start the answer with score value On a scale of 1 to 100 give the repo score based on its complexity  followed by reason why did it deserv that score ?

    Answer:
    """
    # Instr: return a dictionary with the following key 
    # "score":On a scale of 1 to 100 give the repo score based on its complexity 
    # "reason" : why did it deserv that score ?
    prompt_complex = PromptTemplate(
        template=template,
        input_variables=["repo_name", "github_url", "conversation_history", "question", "numbered_documents", "file_type_counts", "filenames"]
    )
    llm_chain = LLMChain(prompt=prompt_complex, llm=llm)


    repos_complexity_dict=[]
    prompt_template = """Write a concise summary of the following:
    {text}:"""

    PROMPT = PromptTemplate(template=prompt_template, 
                            input_variables=["text"])

    ## with intermediate steps
    chain_sum = load_summarize_chain(llm=llm, 
                                chain_type="map_reduce", 
                                return_intermediate_steps=False, 
                                map_prompt=PROMPT, 
                                combine_prompt=PROMPT)



    text_splitter = CharacterTextSplitter()
    return text_splitter, llm_chain,chain_sum, model_name

    
