import streamlit as st
import os
import json


# Page title
st.set_page_config(page_title='🦜🔗 Github Repo Quality Inspector')
st.title('🦜🔗 Github Repo Quality Inspector')
result=''
github_link=st.text_input('Enter Github Profile Link or username', type = 'default')
github_link=os.path.basename(github_link)
git_api_url='https://api.github.com/users/'
with st.form('summarize_form', clear_on_submit=True):
    submitted = st.form_submit_button('Submit')
    if submitted and len(github_link)>0:
        
        list_repo=[]
        try:
            #print(github_link)
            github_link=os.path.join(git_api_url,github_link,'repos')
            #print("******************************")
            result = os.popen("curl "+github_link).read()
            
            #print(result)
            json_object = json.loads(result)
            for count,i in enumerate(json_object):
                if i['visibility']=='public':
                    list_repo.append(i['html_url'])
            #print(list_repo)
        except:
            list_repo['Please enter a correct github link']



#if len(result):
st.info(list_repo)
