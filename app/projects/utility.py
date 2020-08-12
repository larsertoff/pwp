import requests
import flask

# Make some class to query github graphql

headers = {"Authorization": "Bearer YOUR API KEY"}

class GithubQuery:
    '''
    Class to query github graphql also to keep info on 
    '''
    def __init__(self):
        self.github_token = flask.current_app.config['GITHUB_TOKEN']
        self.headers = {"Authorization": "token " + self.github_token}
        self.url = 'https://api.github.com/graphql'
        self.login = self.run_query("""{viewer { login}}""")['data']['viewer']['login']


    def run_query(self, query):
        '''
        Return json for query for github graphql
        '''
        request = requests.post(self.url, json={'query': query}, headers=self.headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

    def set_node_content_as_attribute(self, node_dict):
        pass
