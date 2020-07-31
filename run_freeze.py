from app import create_app
import flask_frozen

freezer = flask_frozen.Freezer(create_app(True))

if __name__ == '__main__':
    freezer.freeze()