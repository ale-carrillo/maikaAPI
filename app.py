from flask import Flask
from flask_cors import CORS
from models.reservation_model import ReservationModel
from services.reservation_service import ReservationService
from schemas.reservation_schemas import ReservationSchema
from routes.reservation_routes import ReservationRoute
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)
db_conn = ReservationModel()
db_conn.connect_to_database()
reservation_service = ReservationService(db_conn)
reservation_schema = ReservationSchema()
reservation_routes = ReservationRoute(reservation_service, reservation_schema)
app.register_blueprint(reservation_routes)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        db_conn.close_connection()