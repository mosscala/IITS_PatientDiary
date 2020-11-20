from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    # if not loggedin:
    return redirect(url_for("login"))
    #else: redirect to dashboard
        #return redirect("dashboard")

@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/history")
def history():
    return render_template("history.html")

@app.route("/appointments")
def appointments():
    return render_template("appointments.html")

@app.route("/howareyou")
def howareyou():
    return render_template("howareyou.html")

@app.route("/medication")
def medication():
    return render_template("medication.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/logout")
def logout():
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(port=1337, debug=True)