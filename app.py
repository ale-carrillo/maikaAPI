from flask import Flask
from flask_cors import CORS
from models.menu_model import MenuModel
from services.menu_services import MenuService
from schemas.menu_schemas import MenuSchema
from routes.menu_routes import MenuRoutes
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)
db_conn = MenuModel()
db_conn.connect_to_database()
menu_service = MenuService(db_conn)
menu_schema = MenuSchema()
menu_routes = MenuRoutes(menu_service, menu_schema)
app.register_blueprint(menu_routes)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        db_conn.close_connection()