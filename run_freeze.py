from app import create_app
import flask_frozen
from flask import url_for

freezer = flask_frozen.Freezer(create_app(config_file_name = 'prod_config.py'))

# Freeze generator

@freezer.register_generator
def product_details():
    for product in ['random', 'repo']:
        yield url_for('projects.projects_specific', repo = product)


if __name__ == '__main__':
    freezer.freeze()