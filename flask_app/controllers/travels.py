from flask_app import app
from flask import render_template , request , redirect, session

from flask_app.models.travel import Travel
from flask_app.models.user import User



@app.route("/trips/new")
def new_page():
    data = request.form
    logged_user = User.get_by_id({'id' : session['user_id']})
    current_user = User.get_by_id(data)
    return render_template("create_trips.html" , logged_user = logged_user.first_name , username = current_user)



@app.route("/trips/create" , methods = ['POST'])
def add_trips():
    data = request.form
    Travel.create(data)
    if not Travel.validate_trip(data):
        return redirect("/trips/new")
    
    return redirect ('/dashboard')




@app.route("/trips/<int:id>/delete")
def delete(id):
    data= {'id' : id}
    travel = Travel.get_by_id(data)
    if travel.user.id == session['user_id']:
        Travel.delete(data)
    return redirect('/dashboard')




@app.route('/trips/<int:id>/show')
def show_page(id):
    data={'id' : id}
    travel= Travel.get_by_id(data)
    logged_user = User.get_by_id({'id' : session['user_id']})
    return render_template("read_about_trips.html" , travel = travel , logged_user = logged_user.first_name)



@app.route("/trips/<int:id>/edit")
def edit(id):
    data= {'id' : id}
    travel = Travel.get_by_id(data)
    logged_user = User.get_by_id({'id' : session['user_id']})
    return render_template("edit_trips.html" , travel = travel , logged_user = logged_user.first_name)



@app.route("/trips/update" , methods = ['POST'])
def update_trip():
    data=request.form
    Travel.update(data)
    return redirect('/dashboard')




