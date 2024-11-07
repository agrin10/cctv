from flask import redirect , url_for , render_template , request , flash , jsonify
from flask_login import login_user , logout_user
from flask_jwt_extended import  jwt_required  
from .controller import handle_add_zone , handle_retrieves_zone , handle_edit_zone
from src.zone import zone_bp
from src.permissions import permission_required
from src.zone.model import Zone


@zone_bp.route('/')
@permission_required(['view'])
@jwt_required()
def zones():
    page = request.args.get('page', 1, type=int)  
    per_page = 12  
    zones = Zone.query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('zones.html', zones=zones.items, pagination=zones)


@zone_bp.route('/' , methods=['POST'])
@permission_required(['create'])
@jwt_required()
def add_zone():
    zone_name = request.form.get('zone_name')
    zone_desc = request.form.get('zone_desc')

    print(zone_name)
    print(zone_desc)
    success , message = handle_add_zone(zone_name , zone_desc)
    if success:
        flash(message=message)
        return redirect(url_for('zone.zones'))
    else:
        flash(message=message)
        return redirect(url_for('zone.zones'))


@zone_bp.route('/' ,methods=["PATCH"])
@permission_required(['edit'])
@jwt_required()
def edit_zone():
    data = request.get_json()
    old_zone_name = data.get('old_zone_name')
    old_zone_desc=data.get('old_zone_desc')
    zone_name = data.get('new_zone_name')
    zone_desc = data.get('new_zone_desc')

    print(f'{old_zone_desc} and {old_zone_name}\n and name {zone_name} , {zone_desc}')
    success , message = handle_edit_zone(zone_name=old_zone_name , new_name=zone_name , zone_desc=old_zone_desc , new_desc=zone_desc)

    if not success:
        # return redirect(url_for('zone.edit_zone'))
        return jsonify(success=success , message=message) ,400
    # return redirect(url_for('zone.zones'))
    return jsonify(success=success , message=message) , 200

@zone_bp.route('/<zone_id>/cameras')
def get_cameras_in_zone(zone_id):
    zone = Zone.query.filter_by(zone_id=zone_id).first()

    if not zone:
        return jsonify({"message": "Zone not found"}), 404

    cameras = zone.cameras  

    cameras_list = [camera.toDict() for camera in cameras]

    return jsonify({
        "zone": zone.toDict(),  
        "cameras": cameras_list
    })