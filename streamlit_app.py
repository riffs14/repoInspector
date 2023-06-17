import streamlit as st
import os
import json


st.title('🎈 Github Repo Quality Inspector')
st.set_page_config(page_title='🦜🔗 Github Repo Quality Inspector')
st.title('🦜🔗 Github Repo Quality Inspector')
#st.write('Hello world!')
github_link=st.text_input('Github Profile Link', type = 'default')
result = os.popen("curl https://api.github.com/users/riffs14/repos ").read()
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