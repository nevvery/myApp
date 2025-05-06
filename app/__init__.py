from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from config import Config

import os


db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
migrate = Migrate()


def create_app(config=Config) -> Flask:
    template_dir = os.path.join(Config.BASE_DIR, 'templates')

    app = Flask(__name__, template_folder=template_dir)
    app.config.from_object(config)

    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as login_bp
    app.register_blueprint(login_bp)

    from app.admin_panel import bp as admin_bp
    app.register_blueprint(admin_bp)

    return app
