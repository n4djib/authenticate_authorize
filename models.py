from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    active = db.Column(db.Boolean)


