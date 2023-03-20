import re
from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.model.user import User
from flask_app.model.pet import Pet
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def main():
    if not session.get('user'):
        return render_template("login.html")
    if session['user'] > 0:
        user_id = session['user']
        return redirect(f'/landing/{user_id}')
    else:
        return render_template("login.html")
    
@app.route('/createuser', methods=['POST'])
def create_user():
    data = {
        "username" : request.form['username'],
        "email" : request.form['email'],
        "password" : request.form['password'],
        "password2" : request.form['password2']
    }
    if not User.validate_user(data):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "username" : request.form['username'],
        "email" : request.form['email'],
        "password" : pw_hash
    }
    user_id = User.createuser(data)
    session['user'] = user_id
    return redirect(f'/landing/{user_id}')

@app.route('/landing/<int:id>')
def landing(id):
    if session['user'] != id:
        return redirect('/logout')
    user = User.getuser(id)
    print(user)
    return render_template("landing.html", user = user)

@app.route('/login', methods = ['POST'])
def login():
    data = {"email" : request.form['email']}
    user_in_db = User.getbyemail(data)
    if not user_in_db:
        flash('Invalid Email/Password', "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password', "login")
        return redirect('/')
    user = user_in_db.id
    session['user'] = user_in_db.id
    return redirect(f'/landing/{user}')

@app.route('/logout')
def logout():
    session['user'] = 0
    return redirect('/')

@app.route('/edituser/<int:id>')
def edituser(id):
    user = User.getuser(id)
    return render_template("updateuser.html", user = user)

@app.route('/updateuser/<int:id>', methods = ['POST'])
def updateoneuser(id):
    data ={ 
        "id" : id,
        "username" : request.form['username'],
        "email" : request.form['email'],
        "password" : request.form['password'],
        "password2" : request.form['password2']
    }
    user_id = session['user']
    if not User.validate_user(data):
        return redirect(f'/updateuser/{user_id}')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "id" : id,
        "username" : request.form['username'],
        "email" : request.form['email'],
        "password" : pw_hash
    }
    User.updateuser(data)
    user_id = session['user']
    return redirect(f'/landing/{user_id}')




