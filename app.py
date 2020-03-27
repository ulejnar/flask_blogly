"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


@app.route("/users")
def users():
    """List users and show add form """
    users = User.query.all()
    return render_template("user_listing.html", users=users)


@app.route("/users/new")
def generate_form():
    return render_template("form.html")


@app.route("/users/new", methods=["POST"])
def addUser():
    """Add user and redirect to list."""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['profile_img'] or None
    user = User(first_name=first_name, last_name=last_name,
                profile_img=img_url)
    db.session.add(user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>")
def user_information(user_id):
    user = User.query.get_or_404(user_id)
    user_posts = user.posts
    return render_template("user_details.html", user=user, posts=user_posts)


@app.route("/users/<int:user_id>/edit")
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user_edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def user_update(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']  
    user.last_name = request.form['last_name']
    user.profile_img = request.form['profile_img']
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new")
def new_post(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query
    return render_template("post_form.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def create_post(user_id):
    user_id = user_id
    title = request.form['Title']
    content = request.form['Content']
    # tagsAdded = request.form.getlist('CurrentTag')

    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def post_information(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.users
    return render_template("post_details.html", post=post, user=user)


@app.route("/posts/<int:post_id>/edit")
def post_edit(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_edit.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['Title'] 
    post.content = request.form['Content']
    db.session.commit()
    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{post.user_id}")


@app.route("/tags")
def list_tags():
    tags = Tag.query.all()
    return render_template("tags_list.html", tags=tags)


@app.route("/tags/new")
def generate_tag_form():
    return render_template("tag_form.html")


@app.route("/tags/new", methods=["POST"])
def create_tag():
    name = request.form['Name']
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>")
def tag_information(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template("tag_details.html", posts=posts, tag=tag)


@app.route("/tags/<int:tag_id>/edit")
def tag_edit(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag_edit.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def tag_update(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['Name']
    db.session.commit()
    return redirect(f"/tags/{tag_id}")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")
