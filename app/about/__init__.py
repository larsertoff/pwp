import flask

about = flask.Blueprint('about', __name__, template_folder='templates')

from app.about import routes