from flask import Flask
from flask_cors import CORS
from models.order_model import OrderModel
from services.order_service import OrderService
from schemas.order_schemas import OrderSchema
from routes.order_route import OrderRoutes
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)
db_conn = OrderModel()
db_conn.connect_to_database()
order_service = OrderService(db_conn)
order_schema = OrderSchema()
order_routes = OrderRoutes(order_service, order_schema)
app.register_blueprint(order_routes)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        db_conn.close_connection()