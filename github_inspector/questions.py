# 


"""
This file run the language model by providing with prompt and question context.
Here the data is pre-processed and pass to language model
"""
from github_inspector.utils import format_documents
from github_inspector.file_processing import search_documents
from langchain.docstore.document import Document
import json
from tqdm import tqdm
import re

class QuestionContext:
    def __init__(self, index, documents,text_splitter, llm_chain,chain_sum, model_name, repo_name, github_url, conversation_history, file_type_counts, filenames):
        self.index = index
        self.documents = documents
        self.llm_chain = llm_chain
        self.chain_sum=chain_sum
        self.model_name = model_name
        self.repo_name = repo_name
        self.github_url = github_url
        self.conversation_history = conversation_history
        self.file_type_counts = file_type_counts
        self.filenames = filenames
        self.text_splitter=text_splitter

def ask_question(question, context: QuestionContext,hardness=10):

    relevant_docs = search_documents(question, context.index, context.documents, n_results=len(context.documents))

    
    numbered_documents_list = format_documents(relevant_docs,hardness)
    
    score=0
    reason=""
    final_ans={}
    for numbered_documents in numbered_documents_list:
        

  
        question_context = f"This question is about the GitHub repository '{context.repo_name}' available at {context.github_url}. The most relevant documents are:\n\n{numbered_documents}"
 
        try:
            
            
            answer_with_sources = context.llm_chain.run(
                model=context.model_name,
                question=question,
                context=question_context,
                repo_name=context.repo_name,
                github_url=context.github_url,
                conversation_history=[],
                numbered_documents=numbered_documents,
                file_type_counts=context.file_type_counts,
                filenames=[]#context.filenames
            )

            
            answer_with_sources = re.sub(' +', ' ', answer_with_sources)
            # print("ans",answer_with_sources)
            # input("4")
        
            a=list(map(int, re.findall('\d+', answer_with_sources)))
           
            chr_ind=answer_with_sources.rfind('Reason:')
            answer_with_sources = re.sub(r'[0-9]', ' ', answer_with_sources)
            reason=reason+answer_with_sources[chr_ind+len('Reason:'):]
            
            score=score+a[0]

            
        except Exception as e:
    
            if str(e)=='<empty message>':
                return False

            continue

    final_ans['score']=score/len(numbered_documents_list)
    texts = context.text_splitter.split_text(reason)
    docs = [Document(page_content=t) for t in texts]
    output_summary = context.chain_sum({"input_documents": docs}, return_only_outputs=True)
    final_ans['reasons']=output_summary['output_text']

    return final_ans
