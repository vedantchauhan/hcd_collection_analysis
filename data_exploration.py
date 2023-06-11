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
CONNECTION_STRING_ISSUES = config('CONNECTION_STRING')
CONNECTION_STRING_COMMENTS = config('CONNECTION_STRING_COMMENTS')
PROJECT_LIST = []

df = pd.DataFrame()

# Main method
if __name__ == '__main__':
    # getting project list
    PROJECT_LIST = github_project_list.get_project()
    # Mongo Client connection
    client_issues = MongoClient(CONNECTION_STRING_ISSUES)
    db_issues = client_issues.get_database()
    client_comments = MongoClient(CONNECTION_STRING_COMMENTS)
    db_comments = client_comments.get_database()

    '''for p in PROJECT_LIST.items():
        print('Project list key: ' + str(p[0]))
        print('Project list value: ' + str(p[1]))'''

        # getting owner and repo from the url by removing the prefix
        #repo = str(p[1]).removeprefix('https://github.com/')
    collection_names = db_issues.list_collection_names()

    for c in collection_names:

        response_issues = list(db_issues.get_collection(c).find({}).limit(100))
        #print(response_issues)
        response_comments = list(db_comments.get_collection(c).find({}).limit(100))
        #print(response)
        '''for i in response_issues:
            #for c in response_comments:
                #issue_title = i['title']
            issue_body = i['body']
            print(issue_body)
                #print(issue_body)
                #comment_body = c['body']
            dict = { 'git_project': c,
                            'issue_body': issue_body
                             #'comment_body' : comment_body
                             }
            df_dictionary = pd.DataFrame([dict])
            df = pd.concat([df, df_dictionary], ignore_index=True)
            print(df.to_string())'''


        for i in response_issues:
            #for c in response_comments:
                #issue_title = i['title']
            issue_body = i['body']
            issue_number = i['number']
            title = i['title']
            issue_url = i['url']
            comments_url = i['comments_url']
            #print(issue_body)
                #print(issue_body)
            #comment_body = i['body']
            dict = { 'git_project': c, 'issue_number' : issue_number, 'title' : title, 'issue_url' : issue_url, 'comments_url' : comments_url,
                            'issue_body': issue_body
                             #'comment_body' : comment_body
                             }
            df_dictionary = pd.DataFrame([dict])
            df = pd.concat([df, df_dictionary], ignore_index=True)
            #print(df.to_string())

    print(df)
    df = df.applymap(lambda x: x.encode('unicode_escape').
                                   decode('utf-8') if isinstance(x, str) else x)
    df.to_excel("data_exploration_issues_all.xlsx", index=False)










