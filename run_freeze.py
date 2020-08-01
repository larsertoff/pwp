from app import create_app
import flask_frozen

freezer = flask_frozen.Freezer(create_app(config_file_name = dev_config))

if __name__ == '__main__':
    freezer.freeze()