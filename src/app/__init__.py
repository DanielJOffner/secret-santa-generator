from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os

db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__)

    app.secret_key = os.environ.get('FLASK_SECRET_KEY', default='a_very_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('FLASK_DATABASE_URI', default='sqlite:///app.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    bootstrap = Bootstrap(app)

    from .models.name import Name
    from .models.hat import Hat

    db.init_app(app)

    from .views import main_blueprint

    app.register_blueprint(main_blueprint)
    return app
