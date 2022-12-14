import os
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()
#database = 'unequalizer' #os.environ["DB"]
#db_user = 'unequalizer' #os.environ["DB_USER"]
#db_password = 'U7%akuLzX5yt' # os.environ["DB_PASSWORD"]

database = os.environ["DB"]
db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]

app = Flask(__name__, static_url_path='', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{db_user}:{db_password}@127.0.0.1/{database}'

db = SQLAlchemy(app)
migrate = Migrate(app,db)


@migrate.configure
def configure_alembic(config):
    # modify config object
    return config

# class User(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(32))
#     Username = db.Column(db.String(32))
#     email = db.column(db.String(50), nullable=False)
#     Password = db.column(db.String(32), nullable=False)

#     def __repr__(self):
#         return f'User: {self.Username}'


class FilePath(db.Model):
    __tablename__ = 'file_path'
    id = db.Column(db.Integer, primary_key=True)
    original_file_name = db.Column(db.String(50), nullable=False)
    file_type = db.Column(db.String(5), nullable=False)
    copies_made = db.Column(db.Integer)
    edited_file_path = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
