from flask import render_template, request, redirect, url_for, flash
from src.cctv.models.model import Users, db
from flask_login import login_user , logout_user , login_required , current_user
from src import app
from src import login_manager

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)



def registeration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists')
            return redirect(url_for('login'))
    
        new_user = Users(username= username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        db.session.rollback()
        flash('Registration successful. Please log in.')
        return redirect(url_for('index'))
def log_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Users.query.filter_by(username=username).first()
        if user is None:
            flash('Username does not exist')
        elif user.check_password(password):
            login_user(user)
            flash('Logged in successfully')
            return redirect(url_for('index'))
        else:
            flash('Invalid password')


    return render_template('login.html')


def logedout():
    logout_user()
    return redirect(url_for('index'))






