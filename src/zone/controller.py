from .model import Zone , db



def handle_add_zone(zone_name , zone_desc):
    existing_zone = Zone.query.filter_by(zone_name = zone_name).first()
    if existing_zone:
        return False , "entered location already exists"
    new_zone = Zone(zone_name = zone_name , zone_desc = zone_desc)
    db.session.add(new_zone)
    db.session.commit()
    return True , 'zone added successfully'

    
def handle_retrieves_zone():
    try:
        zones = Zone.query.all()
        zones = [Zone.toDict(zones) for zones in zones]
        return zones
    except Exception as e:
        db.session.rollback()
        return False, f'An error occurred: {str(e)}'
    
    
def handle_edit_zone(zone_name ,new_name, zone_desc , new_desc):
    zone = Zone.query.filter_by(zone_name = zone_name).first()
    if not zone:
        return False , "zone does not exist"
    zone.zone_name = new_name
    zone.zone_desc = new_desc
    try:
        db.session.commit()
        return True , 'zone updated successfully'
    except Exception as e:
        db.session.rollback()
        return False , f'An error occurred: {str(e)}'



