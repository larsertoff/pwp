from app import create_app
import flask_frozen
from flask import url_for

freezer = flask_frozen.Freezer(create_app(config_file_name = 'freeze_config.py'))

if __name__ == '__main__':
    freezer.freeze()