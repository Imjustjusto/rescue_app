import re
from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.model.user import User
from flask_app.model.pet import Pet
from os.path import join

UPLOAD_FOLDER = r'C:\Users\imjus\OneDrive\Documents\PA\rescue_app\flask_app\static\media'
ALLOWED_EXTENTIONS = {'pdf', 'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/addlisting')
def addlisting():
    return render_template("addlisting.html")

@app.route('/createpet', methods=['POST'])
def createpet():
    imageupload = request.files['imageone']
    path = join(app.config['UPLOAD_FOLDER'], imageupload.filename)
    imageupload.save(path)
    imageupload2 = request.files['imagetwo']
    path = join(app.config['UPLOAD_FOLDER'], imageupload2.filename)
    imageupload2.save(path)
    data = {
        "name" : request.form['name'],
        "age" : int(request.form['age']),
        "species" : request.form['species'],
        "lifestyle" : request.form['lifestyle'],
        "time" : request.form['time'],
        "date" : request.form['date'],
        "imageone" : imageupload.filename,
        "imagetwo" : imageupload2.filename,
        "description" : request.form['description'],
        "user_id" : session['user']
    }
    if not Pet.validate_pet(data):
        return redirect('/addlisting')
    data = {
        "name" : request.form['name'],
        "age" : request.form['age'],
        "species" : request.form['species'],
        "lifestyle" : request.form['lifestyle'],
        "time" : request.form['time'],
        "date" : request.form['date'],
        "imageone" : imageupload.filename,
        "imagetwo" : imageupload2.filename,
        "description" : request.form['description'],
        "user_id" : session['user']
    }
    user_id = session['user']
    Pet.addpet(data)
    return redirect(f'/landing/{user_id}')

@app.route('/listings')
def listings():
    pets = Pet.getpets()
    return render_template("listings.html", pets= pets)

@app.route('/viewone/<int:id>')
def viewone(id):
    if session['user'] < 1:
        return redirect('/')
    pet = Pet.viewpet(id)
    user = User.getuserbypet(id)
    return render_template("viewpet.html", pet = pet, user = user)

@app.route('/editpet/<int:id>')
def edit(id):
    pet = Pet.viewpet(id)
    return render_template("updatelisting.html", pet = pet)

@app.route('/update/<int:id>', methods = ['POST'])
def update(id):
    imageupload = request.files['imageone']
    path = join(app.config['UPLOAD_FOLDER'], imageupload.filename)
    imageupload.save(path)
    imageupload2 = request.files['imagetwo']
    path = join(app.config['UPLOAD_FOLDER'], imageupload2.filename)
    imageupload2.save(path)
    data = {
        "id" : id,
        "name" : request.form['name'],
        "age" : int(request.form['age']),
        "species" : request.form['species'],
        "lifestyle" : request.form['lifestyle'],
        "time" : request.form['time'],
        "date" : request.form['date'],
        "imageone" : imageupload.filename,
        "imagetwo" : imageupload2.filename,
        "description" : request.form['description'],
        "user_id" : session['user']
    }
    if not Pet.validate_pet(data):
        return redirect('/addlisting')
    data = {
        "id" : id,
        "name" : request.form['name'],
        "age" : request.form['age'],
        "species" : request.form['species'],
        "lifestyle" : request.form['lifestyle'],
        "time" : request.form['time'],
        "date" : request.form['date'],
        "imageone" : imageupload.filename,
        "imagetwo" : imageupload2.filename,
        "description" : request.form['description'],
        "user_id" : session['user']
    }
    user_id = session['user']
    Pet.updatepet(data)
    return redirect(f'/landing/{user_id}')

@app.route('/delete/<int:id>')
def delete(id):
    Pet.deletepet(id)
    return redirect('/')