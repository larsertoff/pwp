import flask
from app.projects import projects
import requests
from app.projects.utility import GithubQuery


@projects.route('/projects/')
def projects_overview():

    # Implement some nice cards one pr public repo
    gitql = GithubQuery()

    # Make a query
    query = """
    { viewer { login }}
    """
    answer = gitql.run_query(query)
    print(answer)

    q2 = """ 
  query{
    user(login: "larsertoff"){
        repositories(first: 100, privacy: PUBLIC){
            nodes{
                name
                createdAt
                url
                homepageUrl
                descriptionHTML
                description
                updatedAT
                projectsURL
                primaryLanguage
                openGraphImageUrl
                project
                projects
                resourcePath

            }
        }
    }
}
"""
    repository_info = gitql.run_query(q2)
    print(repository_info)
    repo_list = repository_info['data']['user']['repositories']['nodes']
    print(repo_list)

    for i in repo_list:
        print(i['name'])

    return flask.render_template('projects_overview.html', repo_list = repo_list)

# The idea is to use this as 
@projects.route('/projects/<repo>/')
def projects_specific(repo = None):

    # Get info on specific repo present nicely

    return flask.render_template('projects_specific.html', repo = repo)
    