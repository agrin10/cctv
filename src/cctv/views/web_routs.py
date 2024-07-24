from src import app
from flask import render_template, request, redirect, url_for, flash
from src.cctv.controllers.controller import registeration 



@app.route('/register' , methods=['POST' , 'GET'])
def register():
    if request.method == 'POST':
        return registeration()
    else:
        return render_template('register.html')
    


