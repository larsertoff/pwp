import flask
from app.about import about

@about.route('/about/')
def about_page():
    return flask.render_template('about.html')
