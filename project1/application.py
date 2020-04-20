import os
import sys
import time

from flask import Flask, session, render_template, request
from userDatabase import  *


app = Flask(__name__)


if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


with app.app_context():
    db.create_all()



@app.route("/")
def index():
    return "<h1>Register</h1>"

@app.route("/register")
def register():
    return render_template("registration.html")


@app.route("/userDetails",methods=["POST"])
def userDetails():
    username=request.form.get("username")
    password=request.form.get("password")

    obj = user.query.filter_by(username = username).first()
    if obj is None:
        usr = user(username = username,  password = password, time = time.ctime(time.time()))
        db.session.add(usr)
        db.session.commit()
    else:
        print()
        return render_template("registration.html", message = "email already exists.")

    return render_template("user.html", username = username) 

@app.route("/admin")

def admin():

    adm = user.query.all()
    return render_template("admin.html", adm = adm)