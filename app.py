from flask import Flask
from blueprints import nav
from blueprints.nav import nav_bp
from blueprints.products import product_bp
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(nav_bp)
    app.register_blueprint(product_bp)

    return app



if __name__ == '__main__':
   create_app()
