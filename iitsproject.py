from flask import Flask, redirect, url_for, render_template, request, session
import sqlite3
from database import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "djfsdjf"

# @app.route("/howareyou",  methods=["POST", "GET"])
# def howareyou():
#     if "medstaff" in session:
#         mdstf = session["medstaff"]
#         graph = createappointmenttable()
#         if request.method == "POST":
#             new_symptom = request.form.get('symptoms')
#             new_wellbeingscore = request.form.get('quantity')
#             newentry(new_wellbeingscore, new_symptom)
#             return redirect(url_for("howareyou", medstaff = str(mdstf)))
#         else:
#             return render_template("howareyou.html", medstaff = str(mdstf))
#     else:
#         return redirect(url_for("login"))

@app.route("/howareyou",  methods=["POST", "GET"])
def howareyou():
    if "medstaff" in session:
        mdstf = session["medstaff"]
        graph = createappointmenttable()
        if request.method == "POST":
            new_symptom = request.form.get('symptoms')
            new_wellbeingscore = request.form.get('quantity')
            userid = session["userid"]
            newentrypatient(new_wellbeingscore, new_symptom, userid)
            return redirect(url_for("howareyou", medstaff = str(mdstf)))
        else:
            return render_template("howareyou.html", medstaff = str(mdstf))
    else:
        return redirect(url_for("login"))


@app.route("/")
def index():
    # if not loggedin:
    return redirect(url_for("login"))
    #else: redirect to dashboard
        #return redirect("dashboard")

@app.route("/login", methods=["POST", "GET"])
def login():
    
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('psw')
        remember = 1 if request.form.get('remember') == 'on' else 0
        if email == fetchemail(email) and password == fetchpassword(email):
            userid = session["userid"] = fetchrowid(email)
            mdstf = session["medstaff"] = fetchmedstaff(email)
            return redirect(url_for("history"))
        if email == fetchemail(email) and password != fetchpassword(email):
            return render_template("login.html", msg = '1')
        if not fetchemail(email):
            return render_template("login.html", msg = '2')
    
    else:
        return render_template("login.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('psw')
        passwordrpt = request.form.get('psw-repeat')
        medstaff = 0
        remember = 1 if request.form.get('remember') == 'on' else 0
        if password != passwordrpt:
            return render_template("signup.html", msg = '2')
        if not fetchemail(email):
            newuser(email, password, remember, medstaff)
            return render_template("signup.html", msg = '3')
        elif fetchemail(email):
            return render_template("signup.html", msg = '1')
    else:
        return render_template("signup.html")

@app.route("/medauth", methods=["POST", "GET"])
def medauth():

    medauthnums = ('1234', '2345', '3456', '4567')
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('psw')
        passwordrpt = request.form.get('psw-repeat')
        authnum = request.form.get('authnum')
        medstaff = 1
        remember = 1 if request.form.get('remember') == 'on' else 0
        if authnum not in medauthnums:
            return render_template("medauth.html", msg = '3')
        if password != passwordrpt:
            return render_template("medauth.html", msg = '2')
        if not fetchemail(email):
            newuser(email, password, remember, medstaff)
            return render_template("medauth.html", msg = '4')
        elif fetchemail(email):
            return render_template("medauth.html", msg = '1')
    else:
        return render_template("medauth.html")

@app.route("/logout")
def logout():
    session.pop("userid", None)
    session.pop("medstaff", None)
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "medstaff" in session:
        mdstf = session["medstaff"]
        return render_template("dashboard.html", medstaff = str(mdstf))
    else:
        return redirect(url_for("login"))

@app.route("/history")
def history():        
    if "medstaff" in session:
        mdstf = session["medstaff"]
        userid = session["userid"]
        graph = createindhistory(userid)
        return render_template("history.html", graph = graph, medstaff = str(mdstf))
    else:
        return redirect(url_for("login"))

@app.route("/appointments")
def appointments():
        if "medstaff" in session:
            mdstf = session["medstaff"]
            graph = createappointmenttable()
            return render_template("appointments.html", graph = graph, medstaff = str(mdstf))
        else:
            return redirect(url_for("login"))

@app.route("/medication")
def medication():
        if "medstaff" in session:
            mdstf = session["medstaff"]
            return render_template("medication.html", medstaff = str(mdstf))
        else:
            return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(port=1337, debug=True)

