from sqlalchemyseeder import ResolvingSeeder
from src import db
import json
from sqlalchemy.orm import Session





def seed_ai_properties():
    from .model import AiProperties
    session = db.session
    seeder = ResolvingSeeder(session)
    seeder.register(AiProperties)

    try:
        # Load new properties from the JSON file with UTF-8 encoding
        with open("src/static/names.json", "r", encoding="utf-8") as file:
            new_properties = json.load(file)

        for property_data in new_properties:
            if property_data['target_class'] == 'AiProperties':
                existing_property = session.query(AiProperties).filter_by(name=property_data['data']['name']).first()
                
                if existing_property:   
                    continue

                new_property = AiProperties(name=property_data['data']['name'], label=property_data['data']['label'])
                session.add(new_property)

        db.session.commit()
        print("AI properties successfully committed to the database.")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
    finally:
        db.session.close()