import flask

main_page = flask.Blueprint('main_page', __name__)

@main_page.route('/')
def index():
    return "This is an example app"

