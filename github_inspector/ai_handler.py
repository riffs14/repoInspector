"""

"""

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
"""
This Function Initialize the Language Model
This require the OpenAI API Key
"""
def initialise_llms(key):
    openai_api_key=key

    llm = OpenAI(openai_api_key=openai_api_key, temperature=0.2,max_retries= 1,)

    template = """
    Repo: {repo_name} ({github_url}) | Conv: {conversation_history} | Docs: {numbered_documents} | Q: {question} | FileCount: {file_type_counts} | FileNames: {filenames}

    Instr : start the answer with score value On a scale of 1 to 100 give the repo score based on its complexity  followed by reason why did it deserv that score ?

    Answer:
    """
    
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


"""
This Functio Recieve the documents and Repo details along with language model, and formulate 
Question and generate Response

"""
def start_inspector(repo,text_splitter,llm_chain,chain_sum,model_name,hardness):
    github_url =repo
    repo_name = github_url.split("/")[-1]
    # print(github_url)
    # input('11')
    err=[]
    with tempfile.TemporaryDirectory() as local_path:

        if clone_github_repo(github_url, local_path):
    
            index, documents, file_type_counts, filenames = load_and_index_files(local_path)

            if index is None:
                # print('Repo is empty')
                # err='Repo is empty'
                answer={
                    'score':0,
                    'reasons':"Repo Empty",
                    'repository':github_url
                }
                return answer,""
                
                #exit()

            
            conversation_history = ""
            question_context = QuestionContext(index, documents,text_splitter, llm_chain,chain_sum, model_name, repo_name, github_url, conversation_history, file_type_counts, filenames)

            try:
         
                answer = ask_question("Rate the techincal complexity of this github repo by comparing it with the top five most techincal complex github repo known to mankind", question_context,hardness)
                
                if answer:
                    answer['repository']=github_url
                else:
                    err='Key exceeded the usage quota'
                    
                # print(answer)
                # input()
                #repos_complexity_dict.append(answer)
                print(GREEN + '\nANSWER\n' + str(answer) + RESET_COLOR + '\n')
                return answer,err
                # #conversation_history += f"Question: {user_question}\nAnswer: {answer}\n"
                # input()
            except Exception as e:
                print(f"An error occurred: {e} or key expired")
                return False,str(e)+" or key expired Please try by changing the key"
                #break

        else:
            print("Failed to clone the repository.")
            answer={
                    'score':0,
                    'reasons':"Failed to Clone the repo Empty",
                    'repository':github_url
                }
            return answer,'Failed to clone the repository.'
            


