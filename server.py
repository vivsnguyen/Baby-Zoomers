from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from sqlalchemy import desc

from datetime import datetime
import os

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db

import requests


app = Flask(__name__)
app.secret_key = "12345"

app.jinja_env.undefined = StrictUndefined



@app.route("/", methods=["GET"])
def index():
    """Show homepage."""

    return render_template("homepage.html")


if __name__ == "__main__":
    app.debug = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
