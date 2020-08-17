import flask
import flask_bootstrap
import os
from flask_bootstrap import Bootstrap
from flask import Flask

def create_app(config_file_name: str) -> flask.Flask:
    '''
    Application factory
    '''
    # Initialize application object
    app = flask.Flask(__name__)

    # Find config file in root folder
    if 'dev' in config_file_name:
        app.config.from_pyfile(os.path.join(os.getcwd(), 'config', config_file_name))
    else:
        app.config.from_pyfile(os.path.join(os.getcwd(), 'config', config_file_name))

    # Use bootstrap 4 for simple styling
    bootstrap = flask_bootstrap.Bootstrap(app)

    # Import main page blueprint
    from app.main_page import main_page
    app.register_blueprint(main_page)

    # Import about page blueprint
    from app.about import about
    app.register_blueprint(about)

    # Import projects page blueprint
    from app.projects import projects
    app.register_blueprint(projects)

    return app
