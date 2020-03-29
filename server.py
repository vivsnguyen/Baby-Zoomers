from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from sqlalchemy import desc

from datetime import datetime
import os

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db
from model import User
from model import Schedule
from model import Type
from model import Activity, ActivityType, ScheduleActivity

import requests


app = Flask(__name__)
app.secret_key = "12345"

app.jinja_env.undefined = StrictUndefined



@app.route("/", methods=["GET"])
def index():
    """Show homepage."""

    return render_template("homepage.html")

@app.route("/log-in", methods=["GET"])
def show_login_form():
    """Show login form or registration button for users."""

    user_id = session.get("user_id")

    if user_id:
        return redirect(f"/user-dashboard/{user_id}")

    return render_template("user-login.html")


@app.route("/log-in", methods=["POST"])
def handle_login():
    """Log-in a user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        flash(f"No account with {email}.")
        return redirect("/log-in")

    if not user.check_password(password):
        flash("Incorrect password.")
        return redirect("/log-in")

    session["user_id"] = user.id
    flash("Login successful.")
    return redirect(f"/user-dashboard/{user.id}")

@app.route("/register", methods=["GET"])
def show_registration_form():
    """Show registration form for users."""

    return render_template("user-register.html")


@app.route("/register", methods=["POST"])
def process_user_registration():
    """Process user registration."""

    username = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    zipcode = request.form.get("zipcode")

    if User.query.filter_by(email=email).first():
        flash("An account with this email already exists.")
        return redirect("/register")

    new_user = User(username=username,
                email=email,
                zipcode=zipcode)

    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    # Log in new user
    session["user_id"] = new_user.id

    flash(f"Successfully registered {username}.")
    return redirect(f"/user-dashboard/{new_user.id}")



@app.route("/logout")
def logout():
    """Log out of a user account."""

    session.clear()
    flash("Logout successful.")

    return redirect("/")

@app.route("/user-dashboard/<int:user_id>")
def show_user_dashboard(user_id):
    """Show a user's dashboard where they can view schedules."""

    if check_authorization(user_id):
        user = User.query.get(user_id)
        schedules = user.playlists

        return render_template("user-dashboard.html",
                                user=user,
                                playlists=playlists)

    return render_template("unauthorized.html")


def check_authorization(user_id):
    """Check to see if the logged in user is authorized to view page."""

    # Get the current user's id.
    session_user_id = session.get("user_id")

    # If correct user is not logged in, return False.
    if session_user_id != user_id:
        return False

    return True


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
