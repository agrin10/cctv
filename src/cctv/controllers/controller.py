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
        existing_user = Users.query.filter_by(username=username)
        if existing_user:
            flash('Username already exists')
            return redirect(url_for('index'))
    
        new_user = Users(username= username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        db.session.rollback()
        flash('Registration successful. Please log in.')
        return redirect(url_for('index'))

    return render_template('register.html')



