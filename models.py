"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class Users(db.Model):
    '''Users model '''
    __tablename__ = "Users"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200))

    # creating reference to "Post" with backreference that is assigned to value "user" that
    # will be created at run time. Delete user posts, if user is deleted with the help of
    # cascade="all, delete-orphan"
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        """Showing information about user"""
        return f"<Users {self.id} {self.first_name} {self.last_name}>"


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    create_at = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)

    tag = db.relationship('Tag', secondary='post_tags', backref='posts')

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""
        return self.create_at.strftime("%a %b %-d  %Y, %-I:%M %p")

    def __repr__(self):
        """Showing information about post"""
        return f"<Post {self.id} {self.title} {self.content} {self.create_at} {self.user_id}>"

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)

    def __repr__(self):
        """Showing information about tag"""
        return f"<Tag {self.id} {self.name}>"

class PostTag(db.Model):
    __tablename__ = 'post_tags'
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    def __repr__(self):
        """Showing information about user"""
        return f"<PostTag {self.post_id} {self.tag_id}>"