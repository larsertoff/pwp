import flask
from app.projects import projects
import requests
from app.projects.utility import GithubQuery


@projects.route('/projects/')
def projects_overview():

    # Implement some nice cards one pr public repo
    gitql = GithubQuery()

    # Make a query

    return flask.render_template('projects_overview.html')

# The idea is to use this as 
@projects.route('/projects/<repo>/')
def projects_specific(repo = None):

    # Get info on specific repo present nicely

    return flask.render_template('projects_specific.html', repo = repo)
    