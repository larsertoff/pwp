import flask

main_page = flask.Blueprint('main_page', __name__, template_folder='templates')

from app.main_page import routes
