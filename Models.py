import os
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
db = os.get_env("DB")
db_user = os.get_env("DB_USER")
db_password = os.get_env("DB_PASSWORD")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@localhost/{db}'

db = SQLAlchemy(app)


# class User(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(32))
#     Username = db.Column(db.String(32))
#     email = db.column(db.string(50), nullable=False)
#     Password = db.column(db.String(32), nullable=False)

#     def __repr__(self):
#         return f'User: {self.Username}'


class FilePath(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.string(50))
    file_type = db.Column(db.String(5), nullable=False)
    file_path = db.Column(db.string(100), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


if __name__ == "__main__":
    db.create_all()