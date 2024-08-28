from src import app, db
from flask import render_template
from flask_jwt_extended import jwt_required

    

from src.cctv.views.web_routes import * 
from src.cctv.views.api_routes import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True , port=8080 , host='0.0.0.0')