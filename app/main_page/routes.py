import flask
from app.main_page import main_page

@main_page.route('/')
def home_page():
    return flask.render_template('main_page.html')