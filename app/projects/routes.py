import flask
from app.projects import projects
import requests
from app.projects.utility import GithubQuery
import string
from flask import url_for


@projects.route('/projects/')
def projects_overview():

    # Implement some nice cards one pr public repo
    gitql = GithubQuery()

    # Make a query
    query = """
    { viewer { login }}
    """
    answer = gitql.run_query(query)
    gitql.login
    print(answer['data']['viewer']['login'])

    query_all_public_repos = string.Template("""
    query {
        user(login: "${username}"){
            repositories(first: 100, privacy: PUBLIC){
                nodes{
                    name
                    createdAt
                    url
                    descriptionHTML
                    description
                    updatedAt
                    primaryLanguage { 
                    name
                    }
                    resourcePath
                }
            }
        }
    }""")
    
    query_string = str(query_all_public_repos.substitute(username = gitql.login))
    repository_info = gitql.run_query(query_string)
    repo_list = repository_info['data']['user']['repositories']['nodes']

    for i in repo_list:
        print(i)
        print(i['name'])

    return flask.render_template('projects_overview.html', repo_list=repo_list)

# The idea is to use this as


@projects.route('/projects/<repo>/')
def projects_specific(repo=None):

    # Get info on specific repo present nicely

    return flask.render_template('projects_specific.html', repo=repo)
