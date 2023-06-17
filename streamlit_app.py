import streamlit as st
import os
import json


# Page title
st.set_page_config(page_title='🦜🔗 Github Repo Quality Inspector')
st.title('🦜🔗 Github Repo Quality Inspector')
result=''
github_link=st.text_input('Github Profile Link', type = 'default')
with st.form('summarize_form', clear_on_submit=True):
    submitted = st.form_submit_button('Submit')
    if submitted:
        result = os.popen("github_link ").read()
        json_object = json.loads(result)
        list_repo=[]
        for count,i in enumerate(json_object):
            if i['visibility']=='public':
                list_repo.append(i['html_url'])
        #print(list_repo)


if len(result):
    st.info(list_repo)
else:
    "curl not working"