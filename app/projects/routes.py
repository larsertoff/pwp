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
            query {
            repository(name:"${repository}", owner:"${username}"){
                        id
                        name
                        description
                        }
                    }""")

    
    query_string = str(query_specific_repo.substitute(username=gitql.login, repository = repo))
    specific_repository = gitql.run_query(query_string)

    specific_repository = specific_repository['data']['repository']

    query_blog_post_folder = string.Template("""query{
    repository(owner: "${username}", name: "${repository}" ) {
       filename: object(expression: "master:blog_post/") {
      ... on Tree {
        entries {
          name
          }
          }
          }
          }
          }
    """)
    query_string = str(query_blog_post_folder.substitute(username=gitql.login, repository = repo))
    blog_post_folder = gitql.run_query(query_string)
    
    blog_post_folder = blog_post_folder['data']['repository']['filename']

    if blog_post_folder is None:
        print("Something is wrong with the query")

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
    query_string = str(query_specific_file.substitute(username=gitql.login, repository = repo))
    specific_file = gitql.run_query(query_string)

    specific_file = specific_file['data']['repository']['object']

    # Get info on specific repo present nicely

    print(specific_repository)
    print(blog_post_folder)
    print(specific_file)


    # Ensure some healty default if the queries are off
    if [x for x in (specific_repository, blog_post_folder, specific_file) if x is None]:
        # Fix the queries with some default, il rather do it here than in the template
        pass

    return flask.render_template('projects_specific.html', repo=repo, specific_file = specific_file)
