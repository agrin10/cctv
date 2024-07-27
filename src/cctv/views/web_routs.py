from src import app
from flask import render_template, request, redirect, url_for, flash
from src.cctv.controllers.controller import registeration , log_in , logedout



@app.route('/register' , methods=['POST' , 'GET'])
def register():
    if request.method == 'POST':
        return registeration()
    else:
        return render_template('register.html')
    

@app.route('/login',  methods= ['POST','GET'])
def login():
    if request.method == 'POST':
        return log_in()
    return render_template('login.html')

@app.route('/logout')
def logout():
    return logedout()




