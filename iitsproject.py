from flask import Flask, redirect, url_for, render_template, request, session
import sqlite3
from database import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "djfsdjf"

@app.route("/")
def index():
    return redirect(url_for("login"))

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

@app.route("/logout")
def logout():
    session.pop("userid", None)
    session.pop("medstaff", None)
    return redirect(url_for("login"))

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


    
#sign up for medical staff with additional authentication number
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

@app.route("/dashboard")
def dashboard():
    if "medstaff" in session:
        mdstf = session["medstaff"]
        return render_template("dashboard.html", medstaff = str(mdstf))
    else:
        return redirect(url_for("login"))

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

@app.route("/history")
def history():        
    if "medstaff" in session:
        mdstf = session["medstaff"]
        userid = session["userid"]
        graph = createindhistory(userid)
        return render_template("history.html", graph = graph, medstaff = str(mdstf))
    else:
        return redirect(url_for("login"))

# @app.route("/appointments")
# def appointments():
#         if "medstaff" in session:
#             mdstf = session["medstaff"]
#             # if mdstf = 1:
#             #     return render_template("create_appointement.html")
#             graph = createappointmenttable()
#             return render_template("appointments.html", graph = graph, medstaff = str(mdstf))
#         else:
#             return redirect(url_for("login"))

@app.route("/appointments", methods=["POST", "GET"])
def appointments():
    if "medstaff" in session:
        mdstf = session["medstaff"]
        u_id = session["userid"]
        table = createplotlytable(uid=u_id)
        #appointments_info = fetchappoinment(user_id)
        if request.method == "POST":
            doc_id = session["userid"]
            who = request.form.get('id')
            apptime = request.form.get('time')
            what = request.form.get('what')
            loc = request.form.get('where')
            add_info = request.form.get('add_info')
            link = request.form.get('link')
            recurring = request.form.get('recurring')
            newappointment(who=who, what=what, apptime=apptime, loc=loc, recurring=recurring, additinfo=add_info, videolink=link, doc_id=doc_id)
            return render_template("appointments.html", medstaff = str(mdstf), table = table)
        else:
            return render_template("appointments.html", medstaff = str(mdstf), table = table)
            #return render_template(url_for(display_appointments))
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

