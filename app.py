"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

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
    img_url = request.form['profile_img']
    user = User(first_name=first_name, last_name=last_name, profile_img=img_url)   
    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>")
def user_infromation(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)

@app.route("/users/<int:user_id>/edit")
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user_edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def user_update(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']  
    user.last_name = request.form['last_name']
    user.img_url = request.form['profile_img']
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>/delete")
def delete(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")