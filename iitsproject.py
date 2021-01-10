from flask import Flask, redirect, url_for, render_template, request, session
import sqlite3
from database import fetchhistory, fetchemail, fetchmedstaff, fetchpassword, fetchrowid, createappointmenttable, createindhistory, createmedtable, newentrypatient, newuser, newentrymed

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
        #remember = 1 if request.form.get('remember') == 'on' else 0
        if email == fetchemail(email) and password == fetchpassword(email):
            session["userid"] = fetchrowid(email)
            session["medstaff"] = fetchmedstaff(email)
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
        #graph = createappointmenttable()
        if request.method == "POST":
            new_symptom = request.form.get('symptoms')
            new_wellbeingscore = request.form.get('quantity')
            if mdstf == 0:
                patid = session["userid"]
            elif mdstf == 1:
                patid = request.form.get('patid')
            newentrypatient(new_wellbeingscore, new_symptom, patid)
            return redirect(url_for("howareyou", medstaff = str(mdstf)))
        else:
            return render_template("howareyou.html", medstaff = str(mdstf))
    else:
        return redirect(url_for("login"))

@app.route("/history", methods=["POST", "GET"])
def history():        
    if "medstaff" in session:
        mdstf = session["medstaff"]
        userid = session["userid"]
        if mdstf == 0:
            graph = createindhistory(userid)
            return render_template("history.html", graph = graph, medstaff = str(mdstf))
        elif mdstf == 1:
            if request.method == "POST":
                patid = request.form.get('patid')
                graph = createindhistory(patid)
                return render_template("history.html", graph = graph, showgraph = '1', medstaff = str(mdstf))
            else:
                return render_template("history.html", medstaff = str(mdstf))
                    
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

@app.route("/medication", methods=["POST", "GET"])
def medication():
        if "medstaff" in session:
            mdstf = session["medstaff"]
            if request.method == "POST":
                patid = request.form.get("patid")
                medstaffid = session["userid"]
                medname = request.form.get("medname")
                medbrand = request.form.get("medbrand")
                admroute = request.form.get("admroute")
                dose = request.form.get("dose")
                indic = request.form.get("indic")
                morning = request.form.get("morning")
                noon = request.form.get("noon")
                evening = request.form.get("evening")
                night = request.form.get("night")
                addinfo = request.form.get("addinfo")
                newentrymed(patid, medstaffid, medname, medbrand, admroute, dose, indic, morning, noon, evening, night, addinfo)
                #return render_template("medication.html", medstaff = str(mdstf))
                return render_template("medication.html", table = createmedtable(patid), showtable = '1',  medstaff = str(mdstf))
            else:
                patid = session["userid"]
                table = createmedtable(patid)
                return render_template("medication.html", table = table, medstaff = str(mdstf))
        else:
            return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(port=1337, debug=True)

