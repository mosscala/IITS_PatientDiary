from flask import Flask, redirect, url_for, render_template, request, session
import sqlite3
from database import createindtable, createusertable, deleteappointmententry, deletewbentry, deletemedentry, fetchhistory, fetchemail, fetchmedstaff, fetchpassword, fetchrowid, createmedtablestaff, createappointmenttable, createappointmenttablestaff, createindhistory, createindhistorystafftable, createmedtable, newentrypatient, newuser, newentrymed, newappointment


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
            mdstf = session["medstaff"] = fetchmedstaff(email)
            session["patidofinterest"] = "Unavailable"
            if mdstf == 1:
                return redirect(url_for("dashboard"))
            else:
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
    session.pop("patidofinterest", None)
    return redirect(url_for("login"))

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('psw')
        passwordrpt = request.form.get('psw-repeat')
        title = 0
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        medstaff = 0
        remember = 1 if request.form.get('remember') == 'on' else 0
        if password != passwordrpt:
            return render_template("signup.html", msg = '2')
        if not fetchemail(email):
            newuser(email, password, remember, medstaff, title, firstname, lastname)
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
        title = request.form.get('title')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        authnum = request.form.get('authnum')
        medstaff = 1
        remember = 1 if request.form.get('remember') == 'on' else 0
        if authnum not in medauthnums:
            return render_template("medauth.html", msg = '3')
        if password != passwordrpt:
            return render_template("medauth.html", msg = '2')
        if not fetchemail(email):
            newuser(email, password, remember, medstaff, title, firstname, lastname)
            return render_template("medauth.html", msg = '4')
        elif fetchemail(email):
            return render_template("medauth.html", msg = '1')
    else:
        return render_template("medauth.html")

@app.route("/dashboard",  methods=["POST", "GET"])
def dashboard():
    if "medstaff" in session:
        mdstf = session["medstaff"]
        if mdstf == 1:
            if request.method == "POST" and request.form["btn_identifier"] == "entrybutton":
                session["patidofinterest"] = request.form.get('patid')
                table = createusertable()
                return redirect(url_for("history"))
                #return render_template("dashboard.html", table = table,  medstaff = str(mdstf))
            else:
                table = createusertable()
                return render_template("dashboard.html", table = table,  medstaff = str(mdstf))
        else:
           return redirect(url_for("history")) 
    else:
        return redirect(url_for("login"))

# @app.route("/howareyou",  methods=["POST", "GET"])
# def howareyou():
#     if "medstaff" in session:
#         mdstf = session["medstaff"]
#         #graph = createappointmenttable()
#         if "patidofinterest" in session:
#             return "Hey" + session["patidofinterest"]
#         if request.method == "POST":
#             new_symptom = request.form.get('symptoms')
#             new_wellbeingscore = request.form.get('quantity')
#             if mdstf == 0:
#                 patid = session["userid"]
#             elif mdstf == 1:
#                 patid = request.form.get('patid')
#             newentrypatient(new_wellbeingscore, new_symptom, patid)
#             return redirect(url_for("howareyou", medstaff = str(mdstf)))
#         else:
#             return render_template("howareyou.html", medstaff = str(mdstf))
#     else:
#         return redirect(url_for("login"))

@app.route("/history", methods=["POST", "GET"])
def history():        
    if "medstaff" in session:
        if session["patidofinterest"] == "Unavailable" and session["medstaff"] == 1:
            return redirect(url_for("dashboard"))
        mdstf = session["medstaff"]
        userid = session["userid"]
        if mdstf == 0:
            if request.method == "POST" and request.form["btn_identifier"] == "newentrybutton":
                new_symptom = request.form.get('symptoms')
                new_wellbeingscore = request.form.get('quantity')
                patid = session["userid"]
                newentrypatient(new_wellbeingscore, new_symptom, patid)
                graph = createindhistory(userid)
                table = createindtable(userid)
                return render_template("history.html", table = table, graph = graph, medstaff = str(mdstf))
            else:
                graph = createindhistory(userid)
                table = createindtable(userid)
                return render_template("history.html", table = table, graph = graph, medstaff = str(mdstf))
        elif mdstf == 1:
            if request.method == "POST":
                if request.form["btn_identifier"] == "deletebutton":
                    patid = session["patidofinterest"]
                    entryid = request.form.get('entryid')
                    deletewbentry(entryid)
                    table = createindhistorystafftable(patid)
                    graph = createindhistory(patid)
                    return render_template("history.html", graph = graph, table = table, medstaff = str(mdstf))
                elif request.form["btn_identifier"] == "newentrybutton":
                    patid = session["patidofinterest"]
                    new_symptom = request.form.get('symptoms')
                    new_wellbeingscore = request.form.get('quantity')
                    newentrypatient(new_wellbeingscore, new_symptom, patid)
                    table = createindhistorystafftable(patid)
                    graph = createindhistory(patid)
                    return render_template("history.html", graph = graph, table = table, medstaff = str(mdstf))
            else:
                patid = session["patidofinterest"]
                table = createindhistorystafftable(patid)
                graph = createindhistory(session["patidofinterest"])
                return render_template("history.html", graph = graph, table = table, medstaff = str(mdstf))
    else:
        return redirect(url_for("login"))

@app.route("/appointments", methods=["POST", "GET"])
def appointments():
    if "medstaff" in session:
        if session["patidofinterest"] == "Unavailable" and session["medstaff"] == 1:
            return redirect(url_for("dashboard"))
        mdstf = session["medstaff"]
        userid = session["userid"]
        #appointments_info = fetchappoinment(user_id)
        if request.method == "POST":
            if request.form["btn_identifier"] == "deletebutton":
                patid = (session["patidofinterest"])
                entryid = request.form.get('entryid')
                deleteappointmententry(entryid)
                table = createappointmenttablestaff(patid)
                return render_template("appointments.html", table = table, medstaff = str(mdstf))
            elif request.form["btn_identifier"] == "newentrybutton":
                medstaffid = session["userid"]
                patid = (session["patidofinterest"])
                apptime = request.form.get('date') + " " + request.form.get('time')
                procedure = request.form.get('procedure')
                loc = request.form.get('loc')
                addinfo = request.form.get('addinfo')
                link = request.form.get('link')
                newappointment(apptime, loc, procedure, link, addinfo, patid, medstaffid)
                table = createappointmenttablestaff((session["patidofinterest"]))
                return render_template("appointments.html", table = table,  medstaff = str(mdstf))
                #return render_template("appointments.html", medstaff = str(mdstf), table = createappointmenttable(uid=who), showtable = '1')
        else:
            if mdstf == 1:
                table = createappointmenttablestaff((session["patidofinterest"]))
                return render_template("appointments.html", medstaff = str(mdstf), table = table)
            else:
                table = createappointmenttable(userid)
                return render_template("appointments.html", medstaff = str(mdstf), table = table)
            #return render_template(url_for(display_appointments))
    else:
         return redirect(url_for("login")) 

@app.route("/medication", methods=["POST", "GET"])
def medication():
        if "medstaff" in session:
            if session["patidofinterest"] == "Unavailable" and session["medstaff"] == 1:
                return redirect(url_for("dashboard"))
            mdstf = session["medstaff"]
            if mdstf == 1:
                if request.method == "POST":
                    if request.form["btn_identifier"] == "deletebutton":
                        patid = (session["patidofinterest"])
                        entryid = request.form.get('entryid')
                        deletemedentry(entryid)
                        table = createmedtablestaff(patid)
                        return render_template("medication.html", table = table, medstaff = str(mdstf))
                    elif request.form["btn_identifier"] == "newentrybutton":
                        patid = (session["patidofinterest"])
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
                        return render_template("medication.html", table = createmedtablestaff(patid),  medstaff = str(mdstf))
                else:
                    patid = (session["patidofinterest"])
                    table = createmedtablestaff(patid)
                    return render_template("medication.html", table = table, medstaff = str(mdstf))
            else:
                patid = session["userid"]
                table = createmedtable(patid)
                return render_template("medication.html", table = table, medstaff = str(mdstf))
        else:
            return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(port=1337, debug=True)

