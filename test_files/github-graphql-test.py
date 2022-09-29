import os
import requests

git_key = os.environ.get("GIT_KEY")

headers = {"Authorization": "Bearer " + git_key}

def main():
    

def run_query(self, query, variables): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables}, headers=self.headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))