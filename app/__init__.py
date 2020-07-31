import flask
import os

def create_app(config: bool) -> flask.Flask:
    '''
    Application factory
    '''

    app = flask.Flask(__name__, instance_relative_config=True)

    # Find config file in root folder
    if config:
        app.config.from_pyfile(os.path.join(os.getcwd(), 'config', 'dev_config.py'))
    else:
        app.config.from_pyfile(os.path.join(os.getcwd(), 'config', 'prod_config.py'))

    # Import main page blueprint
    from app.main_page import main_page
    app.register_blueprint(main_page)

    return app
