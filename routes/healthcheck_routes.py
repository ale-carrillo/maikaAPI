from flask import Blueprint, jsonify
from flasgger import swag_from

# Routes for Healthcheck
class HealthcheckRoutes(Blueprint):
    def __init__(self):
        super().__init__('healthcheck', __name__)
        self.register_routes()

    # Routes
    def register_routes(self):
        self.route('/healthcheck', methods=['GET', 'OPTIONS'])(self.healthcheck)
    
  
    @swag_from({
        'tags': ['Health'],
        'responses': {
            200: {
                'description': 'Service is up and running',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'status': {'type': 'string'}
                    }
                }
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    # Veriifying a healthcheck
    def healthcheck(self):
        return jsonify({ 'status': 'up' }), 200