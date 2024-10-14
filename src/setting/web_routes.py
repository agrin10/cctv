from flask import  render_template 
from flask_jwt_extended import  jwt_required  
from src.setting import setting_bp
from src.permissions import permission_required


@setting_bp.route('/')
@permission_required(['view'])
@jwt_required()
def setting():
    return render_template('setting.html')