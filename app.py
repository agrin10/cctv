from src import app, db
from flask import render_template, request, Response


@app.route('/')
def index():
    return render_template('index.html')
    

from src.cctv.views.web_routs import * 
from src.cctv.views.api_routs import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)