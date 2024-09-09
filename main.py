"""
PHQ Studios Ghost Name Picker developed by Stepan Sopin
"""

import random
import secrets
import os
from functools import wraps
from flask import Flask, url_for, redirect, session, render_template, request
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from modules import (
    convert_to_dict,
    reserve_names,
    get_free_names,
    get_taken_names,
    clear_old_ghost_name,
    set_new_ghost_name,
)


# Loading local .env vars
load_dotenv()

# Setting up Flask
app = Flask(__name__)
app.secret_key = secrets.token_hex()

# Setting up OAuth
oauth = OAuth(app)
google = oauth.register(
    name="google",
    # Collect client_id and client secret from google auth api
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    client_kwargs={"scope": "openid email profile"},
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
)


# Converting the csv into a workable dict list for demo purposes
# This should be Datastore instead
ghost_dict_list = convert_to_dict("ghost names.csv")
# ghost_dict_list is global and is mutated through various
# functions and only used for the demo app

# Populate with dummy data, only ran once otherwise it would duplicate names
reserve_names(ghost_dict_list)


# Basic login_required decorator that checks if email is in session data
# Better implementation would be to have a user stored in flask.g as in the docs
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if dict(session).get("email") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# Default route
@app.route("/")
def index():
    # Get taken and available names, separated to display taken ones at the top
    taken_names = get_taken_names(ghost_dict_list)
    free_names = get_free_names(ghost_dict_list)

    # Check session to see if user has set ghost name previously
    ghost_name = dict(session).get("ghost_name", "")

    return render_template(
        "index.html",
        taken=taken_names,
        free=free_names,
        ghost_name=ghost_name,
        title="Ghostly",
    )


# Form to enter name, requiring authentication before being able to visit the page
@app.route("/form")
@login_required
def form():
    # Get full name to populate fields if user has already gone through auth
    first_name = dict(session).get("chosen_first", "")
    family_name = dict(session).get("chosen_family", "")

    name = (first_name, family_name)
    return render_template("form.html", name=name, title="Please enter your name")


# Ghost name selection route
@app.route("/name-select", methods=["POST", "GET"])
def name_select():

    # Store provided names in the session to use to store alongside email and ghost name
    first_name = request.form["first_name"]
    session["chosen_first"] = first_name

    family_name = request.form["family_name"]
    session["chosen_family"] = family_name

    # Generate 3 new random available names
    available_names = get_free_names(ghost_dict_list)
    name_selection = random.sample(available_names, k=3)
    name = (first_name, family_name)

    return render_template(
        "name-select.html",
        name=name,
        ghost_names=name_selection,
        title="Please select your name",
    )


# Load data into CSVDB
@app.route("/submit", methods=["POST", "GET"])
def submit():
    # Don't want to execute the code if we refreshed the page
    if request.method == "POST":
        # Get the ghost name selected and keep in session
        ghost_name = request.form["ghost_name"]
        session["ghost_name"] = ghost_name

        # Get the name and email from session
        first_name = dict(session).get("chosen_first", "")
        family_name = dict(session).get("chosen_family", "")
        email = dict(session).get("email", "")

        # If user held a ghost name previously, this would clear it
        clear_old_ghost_name(ghost_dict_list, email)

        # Set new ghost name
        user_data = (first_name, ghost_name, family_name, email)
        set_new_ghost_name(ghost_dict_list, user_data)

    return redirect(url_for("index"))


# Login page route to redirect to google auth
@app.route("/login")
def login():
    google = oauth.create_client("google")
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


# Auth route
@app.route("/authorize")
def authorize():
    google = oauth.create_client("google")
    token = google.authorize_access_token()
    resp = google.get("userinfo")
    resp.raise_for_status()
    user_info = resp.json()
    session["email"] = user_info["email"]
    session["given_name"] = user_info["given_name"]
    session["family_name"] = user_info["family_name"]
    return redirect("form")


# Logout route, currently only available by manually going to /logout
@app.route("/logout")
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
