from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from sqlalchemy import create_engine 

db = SQLAlchemy()
app = Flask(__name__)
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "SHK"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    db.init_app(app)

    
    from .veiw import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .model import User, Note

    with app.app_context():
        db.create_all()
        print("create database")
        
    login_manager = LoginManager()
    login_manager.login_view= 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app

def create_database():
    engine = create_engine("sqlite:///database.db")
    db.metadata.create_all(bind=engine)
    print('Created database')