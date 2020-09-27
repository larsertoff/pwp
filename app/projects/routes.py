import flask
from app.projects import projects
import requests
from app.projects.utility import GithubQuery
import string
from flask import url_for
import markdown
import markdown2

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
                        createdAt
                        url
                        primaryLanguage {
                        name
                        }
                    }
                }""")

    
    query_string = str(query_specific_repo.substitute(username=gitql.login, repository = repo))
    specific_repository = gitql.run_query(query_string)

    specific_repository = specific_repository['data']['repository']

    # Look for a file named main.json
    query_specific_file=string.Template("""{
                    repository(owner: "${username}", name: "${repository}" ) {
                    object(expression: "master:README.md") {
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
    print(specific_repository)

    # Ensure some healty default if the queries are off
    if [x for x in (specific_repository, specific_file) if x is None]:
        specific_file = {'text':"""# Work in progress"""}

    markdown_text = specific_file['text']

    markdown_html = markdown.markdown(markdown_text, extensions = ['codehilite', 'fenced_code'])
    print(markdown_html)

    markdown2_html = markdown2.markdown(markdown_text, extras =["fenced-code-blocks"])
    print(markdown2_html)

    return flask.render_template('projects_specific.html', repo=repo, markdown_html = markdown_html, 
    mark2_html = markdown2_html, specific_repository = specific_repository)
