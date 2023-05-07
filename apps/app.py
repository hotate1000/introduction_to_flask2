from flask import Flask;
from apps.crud import views as crud_views;

from pathlib import Path;
from flask_migrate import Migrate;
from flask_sqlalchemy import SQLAlchemy;


db = SQLAlchemy();

def create_app():
    app = Flask(__name__);
    # SQLAlchemyとアプリを連携する。
    db.init_app(app);
    # Migrateとアプリを連携する。
    Migrate(app, db);
    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    return app;
