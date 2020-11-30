from flask import Flask, redirect, url_for, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, Email, email_validator

app = Flask(__name__)
app.config['SECRET_KEY'] = "djfsdjf"

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid e-mail'), Length(min=4, max=80)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password1 = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    password2 = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    mptoggle = BooleanField('Not a patient?')

@app.route("/")
def index():
    # if not loggedin:
    return redirect(url_for("login"))
    #else: redirect to dashboard
        #return redirect("dashboard")

@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        return '<h1>' + form.username.data + ' ' + form.password.data + ' ' + str(form.remember.data) + '</h1>'

    return render_template("login.html", form=form)

@app.route("/signup", methods=["POST", "GET"])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        return '<h1>' + form.username.data + ' ' + form.password1.data + ' ' + form.password2.data + ' ' + str(form.mptoggle.data) + ' ' + form.email.data + '</h1>'
    
    return render_template("signup.html", form=form)

@app.route("/logout")
def logout():
    return redirect(url_for("login"))

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

if __name__ == "__main__":
    app.run(port=1337, debug=True)