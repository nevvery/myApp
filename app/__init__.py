from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_security import Security, SQLAlchemyUserDatastore
from flask_migrate import Migrate

from config import Config

import os

db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()


def create_app(config=Config) -> Flask:
    template_dir = os.path.join(config.BASE_DIR, 'templates')

    app = Flask(__name__, template_folder=template_dir)
    app.config.from_object(config)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)

    login.init_app(app)
    login.login_view = 'auth.login'

    migrate.init_app(app, db)

    from app.auth import bp as login_bp
    app.register_blueprint(login_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.admin_panel import bp as admin_bp
    app.register_blueprint(admin_bp)

    from app.payment import bp as payment_bp
    app.register_blueprint(payment_bp)

    from app.security import user_datastore
    security = Security(app, user_datastore, register_blueprint=True)

    return app
