from flask_frozen import Freezer
from app import create_app
import flask_frozen

#freezer = flask_frozen.Freezer(create_app)

if __name__ == '__main__':
    app = create_app(config = True)
    app.run()
    #freezer.freeze()