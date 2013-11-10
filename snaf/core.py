import hashlib

from snaf import app

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager

snaf_hash = hashlib.md5("snaf").hexdigest()

db = SQLAlchemy(app)

api_manager = APIManager(app, flask_sqlalchemy_db=db)