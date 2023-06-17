# app.py
from main import main
import os
import json

if __name__ == "__main__":
    os.environ['OPENAI_API_KEY~']='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'
    github_link='https://api.github.com/users/riffs14/repos'
    result = os.popen("curl https://api.github.com/users/riffs14/repos ").read()
    json_object = json.loads(result)

    list_repo=[]
    for count,i in enumerate(json_object):
        if i['visibility']=='public':
            list_repo.append(i['html_url'])
    #list_repo=['https://github.com/riffs14/blog.git','https://github.com/riffs14/YouTubeLI.git']
    main(list_repo)