"""Blogly application."""
from flask import Flask, render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users, Post, Tag, PostTag

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
    posts = Post.query.order_by(Post.create_at.desc()).limit(10).offset(0).all()
    return render_template("home.html", posts=posts)


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
    flash("Please fill out required fields", "error")
    return redirect("/users/new")


# --------------------------------------404 page--------------------------------------------


@app.errorhandler(404)
def serve_404(e):
    """Render 404 page"""
    return render_template("404.html"), 404


# --------------------------------------User profile page--------------------------------------------
@app.route("/users/<int:user_id>")
def show_user_page(user_id):
    """Show user profile page"""
    user = Users.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user.id).order_by(Post.create_at.desc())
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
    flash("Please fill out required fields", "error")
    return redirect(f"/users/{user_id}/edit")


@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete current user"""
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")


# --------------------------------------User posts--------------------------------------------


@app.route("/users/<int:user_id>/posts/new")
def new_post_form(user_id):
    """Show form for creating a new blog post"""
    user = Users.query.get_or_404(user_id)
    return render_template("posts/new_post.html", user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def create_new_post(user_id):
    """Handling of creation of new blog post"""
    # check if title and content are filled out
    if request.form["title"] and request.form["content"]:
        title = request.form["title"]
        content = request.form["content"]
        # create new post
        new_post = Post(
            title=title,
            content=content,
            user_id=user_id,
        )
        db.session.add(new_post)
        db.session.commit()
        # getting a list of tags
        tags = request.form.getlist("tags")
        for tag in tags:
            # check if tag already exists in the Tag datatable
            # if the tag exists assign it to current post through PostTag relationship datatable
            if Tag.query.filter(Tag.name == tag).first():
                tag_to_add = Tag.query.filter(Tag.name == tag).first()
                post_tag = PostTag(post_id=new_post.id, tag_id=tag_to_add.id)
                db.session.add(post_tag)
                db.session.commit()
            else:
                # if the tag does not exist in the Tag datatable
                # then assign newly created tag to the blog through PostTag relationship datatable
                new_tag = Tag(name=tag)
                db.session.add(new_tag)
                db.session.commit()
                post_tag = PostTag(post_id=new_post.id, tag_id=new_tag.id)
                db.session.add(post_tag)
                db.session.commit()
        return redirect(f"/users/{user_id}")
    flash("Please fill out required fields", "error")
    return redirect(f"/users/{user_id}/posts/new")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show blog post using post_id"""
    post = Post.query.get_or_404(post_id)
    user = Users.query.get(post.user_id)
    # we can get tags assigned to the post because we have a through relationship set up
    # Post datatable is connected to Tag datatable through PostTag relationsihp table
    post_tags = post.tag
    return render_template(
        "posts/view_post.html", post=post, user=user, post_tags=post_tags
    )


@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    """Show edit post form"""
    post = Post.query.get_or_404(post_id)
    user = Users.query.get(post.user_id)
    # we can get tags assigned to the post because we have a through relationship set up
    # Post datatable is connected to Tag datatable through PostTag relationsihp table
    post_tags = post.tag
    return render_template(
        "posts/edit_post.html", post=post, user=user, post_tags=post_tags
    )


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def save_edited_post(post_id):
    """Handle saving blog post after editing is done"""
    # check if title and content are filled out
    if request.form["title"] and request.form["content"]:
        # update post with new information
        post = Post.query.get_or_404(post_id)
        post.title = request.form["title"]
        post.content = request.form["content"]
        db.session.add(post)
        db.session.commit()
        # get a list of tags
        tags = request.form.getlist("tags")
        for tag in tags:
            # setting existing_post_tag for loop scope so if statement scopes could
            # alter it and access it
            existing_post_tag = None
            # check if tag exists else create a new tag
            # if tag exists check if relationship with the current blog exists
            # if relationship exists assign it to existing_post_tag variable
            # if relationship does not exist then create it
            existing_tag = Tag.query.filter(Tag.name == tag).first()
            if existing_tag:
                existing_post_tag = PostTag.query.filter(
                    PostTag.post_id == post.id, PostTag.tag_id == existing_tag.id
                ).first()
            else:
                new_tag = Tag(name=tag)
                db.session.add(new_tag)
                db.session.commit()
                existing_tag = new_tag
            if not existing_post_tag:
                post_tag = PostTag(post_id=post.id, tag_id=existing_tag.id)
                db.session.add(post_tag)
                db.session.commit()
        return redirect(f"/posts/{post_id}")


@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """Handle deleting the post request"""
    post = Post.query.get_or_404(post_id)
    user = Users.query.get(post.user_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{user.id}")


if __name__ == "__main__":
    app.run(debug=True)
