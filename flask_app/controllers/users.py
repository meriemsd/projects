from flask_app import app
from flask import redirect, render_template, request, flash, session
from flask_bcrypt import Bcrypt

from flask_app.models.user import User
from flask_app.models.travel import Travel

bcrypt = Bcrypt(app)



@app.route("/")
def login():
    return render_template("login.html")



@app.route("/register", methods=["POST"])
def process_register():


    if not User.validate_user(request.form):
        return redirect("/")

    print("-------->", request.form["password"])
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    print("=======>", pw_hash)

    data = {**request.form, "password": pw_hash}

    user_id = User.create(data)
    session["user_id"] = user_id
    return redirect("/")



@app.route("/login", methods=["POST"])
def process_login():

    if not User.validate_login_user(request.form):
        return redirect("/")

    
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        
        flash("Invalid Email/Password", "login")
        return redirect("/")

    
    session["user_id"] = user_in_db.id
    return redirect("/dashboard")


# * View Route
@app.route("/dashboard")
def dash():
    
    if "user_id" not in session:
        return redirect("/")
    
    data = {"id": session["user_id"]}
    
    current_user = User.get_by_id(data)
    print("===> current_user:", current_user)
    travels=Travel.get_all()
    return render_template("dashboard.html", username=current_user , travels=travels)





@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")