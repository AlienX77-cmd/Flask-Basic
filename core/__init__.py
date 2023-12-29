from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager 
from sqlalchemy import MetaData

app = Flask(__name__)
app.config.from_object(Configuration)

# Define the naming convention for the metadata
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

# Create the SQLAlchemy instance with the naming convention applied to the metadata
metadata = MetaData(naming_convention=naming_convention)
db = SQLAlchemy(app, metadata=metadata)

# Initialize Flask-Migrate
migrate = Migrate(app, db, render_as_batch=True)

# Initialize Flask-Login
login = LoginManager(app)
login.login_view = 'auth.login'

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of the app
from .task import task as task_blueprint
app.register_blueprint(task_blueprint)

# Import views and models at the end to avoid circular dependencies
from core import views, models