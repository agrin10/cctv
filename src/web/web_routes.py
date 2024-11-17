from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from src.web import web_bp
from flask import render_template, request, redirect, url_for
from flask_login import login_required

@web_bp.route('/home-page')
@jwt_required()
@login_required
def home_page():
    camera_id = request.args.get('camera_id', 1, type=int)
    current_user = get_jwt_identity()
    if current_user is None:
        return redirect(url_for('users.login'))

    return render_template('camera-view.html')


@web_bp.route('/', methods=['GET'])
def index():
    try:
        verify_jwt_in_request()
        return render_template('camera-view.html')
    except Exception as e:
        return redirect(url_for('users.login'))
