from src import  db ,create_app
from src.cctv.controllers.controller import seed_ai_properties 

app = create_app()



from src.cctv.views.web_routes import * 
from src.cctv.views.api_routes import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_ai_properties()
    app.run(debug=True , port=8080 , host='0.0.0.0')