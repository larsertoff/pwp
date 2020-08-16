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

    query_string = str(query_all_public_repos.substitute(username=gitql.login))
    repository_info = gitql.run_query(query_string)
    repo_list = repository_info['data']['user']['repositories']['nodes']

    # Ensure the one updated latest is first
    sorted(repo_list, key=lambda k: k['updatedAt']).reverse()

    return flask.render_template('projects_overview.html', repo_list=repo_list)


@projects.route('/projects/<repo>/')
def projects_specific(repo=None):

    gitql = GithubQuery()

    query_specific_repo = string.Template("""
            repository(owner: "${username}", name: "${repository}") {
                    name
                    createdAt
                    url
                    descriptionHTML
                    description
                    updatedAt
                    primaryLanguage {
                    name
                    }
                }
            }""")

    
    query_string = str(query_specific_repo.substitute(username=gitql.login, repository = repo))
    specific_repository = gitql.run_query(query_string)
    print(specific_repository)

    query_blog_post_folder = string.Template("""
    repository(owner: "${username}", name: "${repository}" ) {
       filename: object(expression: "master:example/") {
      ... on Tree {
        entries {
          name
          }
          }
          }
          }
    """)
    query_string = str(query_blog_post_folder.substitute(username=gitql.login, repository = repo))
    specific_file = gitql.run_query(query_string)
    print(specific_file)

    # Look for a file named main.json
    query_specific_file=string.Template("""{
                    repository(owner: "${username}", name: "${repository}" ) {
                    object(expression: "master:blog_post/main.json") {
                    ... on Blob {
                    text
                    byteSize
                    }
                }
            }
        }""")
    print(repo)
    query_string = str(query_specific_file.substitute(username=gitql.login, repository = repo))
    print(query_string)
    specific_file = gitql.run_query(query_string)

    print(specific_file)

    # Get info on specific repo present nicely

    return flask.render_template('projects_specific.html', repo=repo)
