"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200))

    def __repr__(self):
        """Showing information about user"""
        return f"<Users {self.id} {self.first_name} {self.last_name}>"

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    create_at = db.Column(db.String())
    user_id = db.Column(db.Text, db.ForeignKey('Users.id'))
