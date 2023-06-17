import streamlit as st
import os
import json
import tempfile
#from github_inspector import main
import github_inspector.main_app as main_app
from stqdm import stqdm

exposure_option=['easy','mild','full']
exposure_dict={'easy':1,'mild':10,'full':500}
# Page title
st.set_page_config(page_title='🦜🔗 Github Repo Quality Inspector')
st.title('🦜🔗 Github Repo Quality Inspector')
result=''
github_link=st.text_input('Enter Github Profile Link or username', type = 'default')
open_ai_key=st.text_input('Enter Your OpenAI API Key ', type = 'password',disabled=not github_link)
exposure_selected=st.selectbox("Select The Mode of Inspector : ",options=exposure_option)
github_link=os.path.basename(github_link)
git_api_url='https://api.github.com/users/'
list_repo=[]

from github_inspector.file_processing import clone_github_repo, load_and_index_files
from github_inspector.questions import ask_question, QuestionContext
from github_inspector.utils import format_user_question
from github_inspector.config import WHITE, GREEN, RESET_COLOR, model_name,openai_api_key

def start_inspector(repo,text_splitter,llm_chain,chain_sum,model_name):
    github_url =repo
    repo_name = github_url.split("/")[-1]

    with tempfile.TemporaryDirectory() as local_path:

        if clone_github_repo(github_url, local_path):
    
            index, documents, file_type_counts, filenames = load_and_index_files(local_path)

            if index is None:
                print('Repo is empty')
                return
                
                #exit()

            
            conversation_history = ""
            question_context = QuestionContext(index, documents,text_splitter, llm_chain,chain_sum, model_name, repo_name, github_url, conversation_history, file_type_counts, filenames)
            #while True:
            try:
                
                user_question =" " #input("\n" + WHITE + "Ask a question about the repository (type 'exit()' to quit): " + RESET_COLOR)
                if user_question.lower() == "exit()":
                    return
                    #break
                #print('Thinking...')
                user_question = format_user_question(user_question)

                answer = ask_question("Rate the complexity of this repo by comparing it with the top five most complex repo known to mankind", question_context,hardness)
                answer['repository']=github_url
                #repos_complexity_dict.append(answer)
                print(GREEN + '\nANSWER\n' + str(answer) + RESET_COLOR + '\n')
                return answer
                # #conversation_history += f"Question: {user_question}\nAnswer: {answer}\n"
                # input()
            except Exception as e:
                print(f"An error occurred: {e}")
                #break

        else:
            print("Failed to clone the repository.")



with st.form('summarize_form', clear_on_submit=True):
    submitted = st.form_submit_button('Submit')
    if submitted and len(github_link)>0:
        
        
        try:
            print(exposure_selected)
            hardness=exposure_dict[exposure_selected]
            #print(github_link)
            github_link=os.path.join(git_api_url,github_link,'repos')
            #print("******************************")
            result = os.popen("curl "+github_link).read()
            
            #print(result)
            json_object = json.loads(result)

            for count,i in enumerate(json_object):
                if i['visibility']=='public':
                    list_repo.append(i['html_url'])
            text_splitter,llm_chain,chain_sum,model_name=main_app.run(open_ai_key)
            final_answer=[]
            for repo_count,repo in stqdm(enumerate(list_repo)):
                if repo_count>1:
                    break
                ans=start_inspector(repo,text_splitter,llm_chain,chain_sum,model_name)
                final_answer.append(ans)

            #print(list_repo)

            final_answer=sorted(final_answer, key=lambda i: i['score'])

        except:
            list_repo.append('Please enter a correct github link')



if len(result):
    if len(list_repo)==0:
        st.info("user has no pulic repo")


    st.info(final_answer[0])
