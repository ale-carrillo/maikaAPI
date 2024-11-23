from flask import Flask
from flask_cors import CORS
from models.staff_model import StaffModel
from services.staff_service import StaffService
from schemas.staff_schema import StaffSchema
from routes.staff_routes import StaffRoutes
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)
db_conn = StaffModel()
db_conn.connect_to_database()
staff_service = StaffService(db_conn)
staff_schema = StaffSchema()
staff_routes = StaffRoutes(staff_service,staff_schema)
app.register_blueprint(staff_routes)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        db_conn.close_connection()