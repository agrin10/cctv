from flask import Blueprint , jsonify ,request
from .controller import handle_add_zone , handle_retrieves_zone
from flask_jwt_extended import jwt_required
from src.zone import zones_bp
from src.permissions import permission_required


@zones_bp.route('/api/add-zone' , methods=['POST'])
@permission_required(['create'])
@jwt_required()
def api_add_zone():
    zone_name = request.json['zone_name']
    zone_desc = request.json['zone_desc']
    success , message = handle_add_zone(zone_name , zone_desc)

    if success:
        return jsonify(message=message , success=success)
    else:
        return jsonify(message=message , success=success)

    

@zones_bp.route('/api/zones')
@permission_required(['view'])
@jwt_required()
def api_zones():
    zones = handle_retrieves_zone()    
    return jsonify(zones = zones)
