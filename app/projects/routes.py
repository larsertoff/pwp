import flask
from app.projects import projects

@projects.route('/projects/')
def projects_overview():
    return flask.render_template('projects_overview.html')