"""Blogly application."""
from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users,Post
from datetime import datetime, date


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blogly.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
# we need to turn app debug mode on.
# app.debug = True

app.config["SECRET_KEY"] = "ThisislikesoSecret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()

@app.route("/")
def home():
    """Showing list of all users and link to add new users"""
    users = Users.query.order_by(Users.last_name, Users.first_name).all()
    return render_template("users/show_all_users.html", users=users)


@app.route("/users")
def show_all_users():
    """Showing list of all users and link to add new users"""
    users = Users.query.order_by(Users.last_name, Users.first_name).all()
    return render_template("users/show_all_users.html", users=users)


@app.route("/users/new")
def new_user_form():
    """Show form to create a new user"""
    return render_template("users/new.html")


@app.route("/users/new", methods=["POST"])
def create_new_user():
    """Handing form submition for creating a new user"""
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    img_url = request.form["img-url"]
    # default_pic = 'static/profile.jpg'
    # img_url = default_pic if not img_url else img_url
    if first_name and last_name:
        new_user = Users(first_name=first_name, last_name=last_name, image_url=img_url)
        db.session.add(new_user)
        db.session.commit()
        return redirect(f"/users")
    return redirect("/users/new")

# --------------------------------------User profile page--------------------------------------------
@app.route("/users/<int:user_id>")
def show_user_page(user_id):
    """Show user profile page"""
    user = Users.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user.id)
    return render_template("users/user_page.html", user=user, posts=posts)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Show form to edit an existing user"""
    user = Users.query.get(user_id)
    return render_template("users/edit_user.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    """Handle form submission for updating an existing user"""
    updated_user = Users.query.get_or_404(user_id)
    if request.form["first-name"] and request.form["last-name"]:
        updated_user.first_name = request.form["first-name"]
        updated_user.last_name = request.form["last-name"]
        updated_user.image_url = request.form["img-url"]
        db.session.add(updated_user)
        db.session.commit()
        return redirect(f"/users/{user_id}")
    return redirect(f"/users/{user_id}/edit")


@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    '''Delete current user'''
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

# --------------------------------------User posts--------------------------------------------

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    user = Users.query.get(user_id)
    posts = Post.query.filter(Post.id == user_id)
    return render_template('posts/new_post.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_new_post(user_id):
    if request.form['title'] and request.form['content']:
        title = request.form['title']
        content = request.form['content']
        current_date = date.today()
        time_and_date = datetime.now()
        time = time_and_date.strftime("%H:%M:%S")
        new_post = Post(title=title, 
                        content=content, 
                        create_at=f'{current_date} - {time}',
                        user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(f'/users/{user_id}')
    return redirect(f'/users/{user_id}/posts/new')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get(post_id)
    user = Users.query.get(post.id)
    return render_template('posts/view_post.html', post=post, user=user)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get(post_id)
    user = Users.query.get(post.id)
    return render_template('posts/edit_post.html', post=post, user=user)

if __name__ == "__main__":
    app.run(debug=True)
