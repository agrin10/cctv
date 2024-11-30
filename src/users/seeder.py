import json
from sqlalchemyseeder import ResolvingSeeder
from src import db

def seed_user_management():
    from .model import Accesses, Module, Permissions
    session = db.session  
    seeder = ResolvingSeeder(session)

    try:
        with open("src/static/user-management.json", 'r', encoding='utf-8') as file:
            new_entities = json.load(file)
            for entry in new_entities:
                target_class = entry["target_class"]
                data = entry["data"]

                print(f"Seeding data for: {target_class}")  

                if target_class == "Module":
                    for item in data:
                        module_name = item["module_name"]
                        existing_module = session.query(Module).filter_by(module_name=module_name).first()
                        if existing_module:
                            print(f"Module with name {module_name} already exists.")
                        else:
                            new_module = Module(module_name=module_name)
                            session.add(new_module)
                            print(f"Added new Module with name {module_name}.")

                elif target_class == "Permissions":
                    for item in data:
                        name = item["name"]
                        label = item.get("label", "")
                        existing_permission = session.query(Permissions).filter_by(name=name).first()
                        if existing_permission:
                            print(f"Permission with name {name} already exists.")
                        else:
                            new_permission = Permissions(name=name, label=label)
                            session.add(new_permission)
                            print(f"Added new Permission with name {name}.")

                elif target_class == "Accesses":
                    for item in data:
                        module_criteria = item["!refs"]["module_id"]["criteria"]
                        permissions_criteria = item["!refs"]["permissions_id"]["criteria"]

                        module = session.query(Module).filter_by(**module_criteria).first()
                        permission = session.query(Permissions).filter_by(**permissions_criteria).first()

                        if module and permission:
                            existing_access = session.query(Accesses).filter_by(module_id=module.module_id, permissions_id=permission.id).first()
                            if existing_access:
                                print(f"Access for module {module.module_name} and permission {permission.name} already exists.")
                            else:
                                new_access = Accesses(module_id=module.module_id, permissions_id=permission.id)
                                session.add(new_access)
                                print(f"Added new Access for module {module.module_name} and permission {permission.name}.")
                        else:
                            print(f"Module or Permission not found for criteria: {module_criteria}, {permissions_criteria}")

        session.commit()
        print("Entities successfully committed to the database.")

    except Exception as e:
        print(f"Error occurred: {e}")
        session.rollback()
    
    finally:
        session.close()


def seed_admin_user():
    from .model import Users, UserAccess, Permissions  ,Accesses
    session = db.session

    try:
        existing_user = session.query(Users).filter_by(username="admin").first()
        password = "admin"
        if not existing_user:
            admin_user = Users(
                username="admin",
                email="admin@example.com", 
                name="Admin",                
                last_name="User",           
            )
            # Set password
            admin_user.set_password(password) 
            
            session.add(admin_user)
            session.commit()  
            
            print("Admin user created.")

            all_permissions = session.query(Permissions).all()
            for permission in all_permissions:
                access = session.query(Accesses).filter_by(permissions_id=permission.id).first()
                if access:
                    user_access = UserAccess(
                        user_id=admin_user.user_id,
                        access_id=access.id
                    )
                    session.add(user_access)

            session.commit()  
            print("All permissions granted to admin user.")

        else:
            print("Admin user already exists, skipping creation.")
    
    except Exception as e:
        print(f"Error occurred while seeding admin user: {e}")
        session.rollback()

    finally:
        session.close()
