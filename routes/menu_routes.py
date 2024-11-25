from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from logger.logger_base import Logger
from flasgger import swag_from

class MenuRoutes(Blueprint):
    def __init__(self, menu_service, menu_schema):
        super().__init__('menu', __name__)
        self.menu_service = menu_service
        self.menu_schema = menu_schema
        self.register_routes()
        self.logger = Logger()

    def register_routes(self):
        self.route('/menu-api/v1/menus', methods=['GET'])(self.get_meals)
        self.route('/menu-api/v1/menus', methods=['POST'])(self.add_meals)
        self.route('/healthcheck', methods=['GET'])(self.healthcheck)
    
    @swag_from({
        'tags': ['meals'],
        'responses': {
            200: {
                'description': 'Get All meals from the menu',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'meal': { 'type': 'string' },
                            'description': { 'type': 'string' },
                            'price': { 'type': 'integer' },
                            'image': { 'type': 'string' },
                        }
                    }
                }
            }
        }
    })

    def get_meals(self):
        meals = self.menu_service.get_all_meals()
        return jsonify(meals), 200
    
    @swag_from({
        'tags': ['Meals'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'meal': { 'type': 'string' },
                        'description': { 'type': 'string' },
                        'price': { 'type': 'integer' },
                        'image': { 'type': 'string' },
                    },
                    'required': ['meal', 'description','price','image' ]
                }
            }
        ],
        'responses': {
            201: {
                'description': 'Meal succesfully added'
            },
            400: {
                'description': 'Invalid data'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })

    def add_meals(self):
        try:
            request_data = request.json

            if not request_data:
                return jsonify({'error': 'invalid data'}), 400
            
            meal = request_data.get('meal')
            description = request_data.get('description')
            price = request_data.get('price')
            image = request_data.get('image')

            try:
                self.menu_schema.validate_meal(meal)
                self.menu_schema.validate_description(description)
                self.menu_schema.validate_price(price)
                self.menu_schema.validate_image(image)
            except ValidationError as e:
                return jsonify({ 'error': 'Invalid data' }), 400

            new_meal = {
                'meal': meal,
                'description': description,
                'price':price,
                'image': image
 
            }

            created_meal = self.menu_service.add_meal(new_meal)
            return jsonify(created_meal), 201
        except Exception as e:
            self.logger.error(f'Error adding new meal to the database: {e}')
            return jsonify({ 'error': f'An exception has ocurred: {e}' }), 500
         
    def healthcheck(self):
        return jsonify({ 'status': 'up' }), 200