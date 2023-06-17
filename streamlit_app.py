#####################################################
# Author        : Rahul Kumar Chaudhary             #
# Email         : rkchaudhary.kvs@gmail.com         #
# git username  : riffs14                           #
#####################################################
"""
This File Contain the UI Logic

"""
# Important Liberary Import
import streamlit as st
import os
import json
import tempfile
import github_inspector.ai_handler as ai_handler
from stqdm import stqdm
from github_inspector import utils
from github_inspector.config import exposure_dict,exposure_option,git_api_url,result
from github_inspector.file_processing import clone_github_repo, load_and_index_files
from github_inspector.questions import ask_question, QuestionContext
from github_inspector.utils import format_user_question
from github_inspector.config import WHITE, GREEN, RESET_COLOR, model_name,openai_api_key

# Stream Line UI Starts Here
# Page title
st.set_page_config(page_title='🦜🔗 Github Repo Quality Inspector')
st.title('🦜🔗 Github Repo Quality Inspector')

############################   Must Have Fields ###########################################
github_link=st.text_input('Enter Github Profile Link or username', type = 'default')
open_ai_key=st.text_input('Enter Your OpenAI API Key ', type = 'password',disabled=not github_link)

st.text("Instruction : Choose the Strictness level. It controll data processing.\n  Below are the details of differece strictness")
st.text("Easy : 70 percent of un-necessary data are discarded. It is faster but less accurate")
st.text("Mild : 50 percent of un-necessary data are discarded. ")
st.text("Easy : agent doesn't discard any data. Slower but accurate. \n Use this if you have unlimited  api access")
exposure_selected=st.selectbox("Select The Strictness of Inspector : ",options=exposure_option)

############################################################################################

github_link=os.path.basename(github_link)

list_repo=[]


flag=False


# Disable the submit button after it is clicked
def disable():
    st.session_state.disabled = True

# Initialize disabled for form_submit_button to False
if "disabled" not in st.session_state:
    st.session_state.disabled = False

# On Submit Button Click
with st.form('summarize_form', clear_on_submit=True):
    submitted = st.form_submit_button('Submit')
    if not open_ai_key.startswith('sk-'):
        st.write('Enter a valid key')

    if submitted and len(github_link)>0 and open_ai_key.startswith('sk-'):
        
        
        try:
    
            hardness=exposure_dict[exposure_selected]
            
            list_repo,result=utils.repo_link_collector(github_link)
            
            text_splitter,llm_chain,chain_sum,model_name=ai_handler.initialise_llms(open_ai_key)
            final_answer=[]
            for repo_count,repo in stqdm(enumerate(list_repo)):
              
                ans=ai_handler.start_inspector(repo,text_splitter,llm_chain,chain_sum,model_name,hardness)
                final_answer.append(ans)

            

            final_answer=sorted(final_answer, key=lambda i: i['score'])

        except:
            result=""
            flag=True
            list_repo.append('Please enter a correct github link')

if submitted and not len(list_repo):
    st.info('User has No wroking Repository')

if flag:
    st.info('Please enter a correct github link')
if len(result):

    st.subheader("Woo!! Most Complex Repo Found")
    st.text("***********************************************************************************")
    st.write({
        "Most Complex Repository : ": os.path.basename(final_answer[0]['repository']),
        "Reason": final_answer[0]['reasons'],
        "Repo Link " : final_answer[0]['repository']
    })
    
    if len(final_answer)>3:
        st.text("***********************************************************************************")
        st.text("Here are rest top Three Repo from the profile ")
        st.write([{
            "Most Complex Repository : ": os.path.basename(final_answer[i]['repository']),
            "Reason": final_answer[i]['reasons'],
            "Repo Link " : final_answer[i]['repository']
        } for i in range(3)])
    st.text("***********************************************************************************")
    st.text("Here is the Weakest  Repo from the profile ")
    st.write({
        "Most Complex Repository : ": os.path.basename(final_answer[-1]['repository']),
        "Reason": final_answer[-1]['reasons'],
        "Repo Link " : final_answer[-1]['repository']
    })


