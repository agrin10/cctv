from flask import redirect , url_for , render_template , request , flash 
from flask_login import login_user , logout_user
from flask_jwt_extended import  jwt_required  
from .controller import handle_add_zone , handle_retrieves_zone
from src.zone import zones_bp
from src.permissions import permission_required


@zones_bp.route('/zones')
@permission_required(['view'])
@jwt_required()
def zones():
    zones= handle_retrieves_zone()
    return render_template('zones.html' , zones=zones)


@zones_bp.route('/add-zone' , methods=['POST' , 'GET'])
@permission_required(['create'])
@jwt_required()
def add_zone():
    if request.method == 'POST':
        zone_name = request.form.get('zone-name')
        zone_desc = request.form.get('zone-desc')
        success , message = handle_add_zone(zone_name , zone_desc)
        if success:
            flash(message=message)
            return redirect(url_for('zone.zones'))
        else:
            flash(message=message)
            return redirect(url_for('zone.add_zone'))
    return render_template('add-zone.html')