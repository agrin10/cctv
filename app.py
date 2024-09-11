from src import  db ,create_app
from flask_jwt_extended import jwt_required , get_jwt_identity ,verify_jwt_in_request 
from flask import request , url_for , render_template ,redirect

app = create_app()

@app.route('/home-page')
@jwt_required()
def home_page():
    camera_id = request.args.get('camera_id', 1, type=int)
    current_user = get_jwt_identity()
    if current_user is None:
        return redirect(url_for('users.login'))  # Redirect if user identity is None
    
    return render_template('base.html', camera_id=camera_id)

@app.route('/', methods=['GET'])
def index():
    try:
        verify_jwt_in_request()
        return render_template('index.html')
    except Exception as e:
        return redirect(url_for('users.login'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True , port=8080 , host='0.0.0.0')