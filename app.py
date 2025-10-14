from flask import Flask
from blueprints import nav
from blueprints.nav import nav_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(nav_bp)
    return app



if __name__ == '__main__':
   create_app()
