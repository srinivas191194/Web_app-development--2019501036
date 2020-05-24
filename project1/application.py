import os
import sys
import time

from flask import Flask, session, render_template, request,redirect,url_for
from userDatabase import  *


app = Flask(__name__)
app.secret_key ='srinivas'


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


@app.route("/logout/<username>")
def logout(username):
    session.pop(username, None)
    return redirect(url_for('index'))


@app.route("/home/<user>")
def userHome(user):

    if user in session:
        return render_template("user.html", username=user)
    
    return redirect(url_for('index'))


@app.route("/auth", methods =["POST", "GET"])
def auth():

    if request.method == "POST":

        username = request.form.get('username')
        usr_password = request.form.get('password')

        userData = user.query.filter_by(username=username).first()

        if userData is not None:
            if userData.username == username and userData.password ==usr_password:
                session[username] = username
                return redirect(url_for('userHome', user = username))
            else:
                return render_template("registration.html", message = "Please enter correct username/password")
        else:

            return redirect(url_for('index'))
    else:

        return "<h1>Please login/register instead</h1>"


# @app.route("/userDetails",methods=["POST"])
# def userDetails():
#     username=request.form.get("username")
#     password=request.form.get("password")

#     obj = user.query.filter_by(username = username).first()
#     if obj is None:
#         usr = user(username = username,  password = password, time = time.ctime(time.time()))
#         db.session.add(usr)
#         db.session.commit()
#     else:
#         print()
#         return render_template("registration.html", message = "email already exists.")

#     return render_template("user.html", username = username) 

@app.route("/userDetails",methods=["POST","GET"])
def userDetails():
    if request.method=='POST':

        userName = request.form.get("username")
        password = request.form.get("password")  
        obj = user.query.filter_by(username=userName).first()
        if obj is None:
            usr = user(username = userName,  password = password, time = time.ctime(time.time()))
            db.session.add(usr)
            db.session.commit()
            return render_template("user.html", username = userName, message = "Succesfully Registered")

        else:
            return render_template("registration.html", message = "user already exists.")

    return "<h1>Please try to register </h1>"

@app.route("/admin")

def admin():

    adm = user.query.all()
    return render_template("admin.html", adm = adm)
