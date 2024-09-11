from flask import Blueprint , jsonify ,request
from .controller import handle_add_zone , handle_retrieves_zone
from flask_jwt_extended import jwt_required
from src.cctv.zone import zones_bp



@zones_bp.route('/api/add-zone' , methods=['POST'])
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
@jwt_required()
def api_zones():
    zones = handle_retrieves_zone()    
    return jsonify(zones = zones)