from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required, get_db_connection, get_session_user, error
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile("config.py")
Session(app)


@app.route("/")
@login_required
def index():
    ...


@app.route("/add_book", methods=["GET", "POST"])
@login_required
def add_book():
    ...


@app.route("/remove_book", methods=["GET", "POST"])
@login_required
def remove_book():
    ...


@app.route("/edit_book", methods=["GET", "POST"])
@login_required
def edit_book():
    ...


@app.route("/add_shelf", methods=["GET", "POST"])
@login_required
def add_shelf():
    ...


@app.route("/remove_shelf", methods=["GET", "POST"])
@login_required
def remove_shelf():
    ...


@app.route("/edit_shelf", methods=["GET", "POST"])
@login_required
def edit_shelf():
    ...


@app.route("/add_book_shelf", methods=["GET", "POST"])
@login_required
def add_book_shelf():
    ...


@app.route("/register", methods=["GET", "POST"])
def register():
    ...


@app.route("/login", methods=["GET", "POST"])
def login():
    ...


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    session.clear()

    return redirect("/")


@app.route("/edit_username", methods=["GET", "POST"])
@login_required
def edit_username():
    ...


@app.route("/edit_email", methods=["GET", "POST"])
@login_required
def edit_email():
    ...


@app.route("/edit_password", methods=["GET", "POST"])
@login_required
def edit_password():
    ...