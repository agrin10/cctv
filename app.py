from src import app, db
from flask import render_template, request, Response
from src.cctv.views import web_routs


@app.route('/')
def index():
    return render_template('index.html')



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)