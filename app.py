from flask import Flask
from flask_cors import CORS
from models.inventory_model import InventoryModel
from services.inventory_service import InventoryService
from schemas.inventory_schema import InventorySchema
from routes.inventory_routes import InventoryRoutes
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)
db_conn = InventoryModel()
db_conn.connect_to_database()
inventory_service = InventoryService(db_conn)
inventory_schema = InventorySchema()
inventory_routes = InventoryRoutes(inventory_service, inventory_schema)
app.register_blueprint(inventory_routes)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        db_conn.close_connection()