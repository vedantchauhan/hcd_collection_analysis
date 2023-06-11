from os import environ
from decouple import config
import requests
import pandas as pd
import github_project_list
from pymongo import MongoClient
import json

#Set encoding
environ["PYTHONCODE"] = "utf-8"

#API variables
GITHUB_API = config('GITHUB_API')
PAT_TOKEN = config('PAT_TOKEN')
CONNECTION_STRING = config('CONNECTION_STRING')
PROJECT_LIST = []
RESPONSE_LIST = []
page = 1
df = pd.DataFrame()

# Repo based issues
def repo_issues(repo, page):

    url = str(GITHUB_API) + "repos/" + repo + "/issues?per_page=100&page=" + str(page) + "&state=all"
    print(url)
    payload={}
    headers = {
      'Accept': 'application/vnd.github+json',
      'Authorization': 'Bearer ' + str(PAT_TOKEN)
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    #print(response.text)
    return response

# Main method
if __name__ == '__main__':
    # getting project list
    PROJECT_LIST = github_project_list.get_project()
    # Mongo Client connection
    client = MongoClient(CONNECTION_STRING)
    db = client.get_database()

    for p in PROJECT_LIST.items():
        print('Project list key: ' + str(p[0]))
        print('Project list value: ' + str(p[1]))

        # getting owner and repo from the url by removing the prefix 
        repo = str(p[1]).removeprefix('https://github.com/')
        print(repo)
        repo_response = repo_issues(repo, page)

        '''RESPONSE_LIST.append(repo_response.text)
        print(repo_response)
        repo_response_page = " "
        page = 1
        if repo_response.text:
            while True:
                page = page + 1
                print(page)
                repo_response_page = repo_issues(repo, page)
                #print(repo_response_page)
                print(len(repo_response_page.content))
                if len(repo_response_page.content) != 2:
                    RESPONSE_LIST.append(repo_response_page.text)
                else:
                    break

        #print(RESPONSE_LIST)'''

        # add records in pandas
        #for r in RESPONSE_LIST:
        df_json = pd.read_json(repo_response.text)
        #df = pd.concat([df, df_json], ignore_index=True)

        print(df_json)

        # add record to the collection
        df_json.fillna("-", inplace=True)
        db.create_collection(p[0]).insert_many(df_json.to_dict('records'))







