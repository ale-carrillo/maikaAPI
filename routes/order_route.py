from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from logger.logger_base import Logger
from flasgger import swag_from


class OrderRoutes(Blueprint):
    def __init__(self, order_service, order_schema):
        super().__init__('order', __name__)
        self.order_service = order_service
        self.order_schema = order_schema
        self.register_routes()
        self.logger = Logger()

    def register_routes(self):
        self.route('/api/v1/orders', methods=['GET'])(self.get_orders)
        self.route('/api/v1/orders', methods=['POST'])(self.add_order)
        self.route('/api/v1/orders/<int:order_id>', methods=['PUT'])(self.update_order)
        self.route('/api/v1/orders/<int:order_id>', methods=['DELETE'])(self.delete_order)
        self.route('/healthcheck', methods=['GET'])(self.healthcheck)

    @swag_from({
        'tags': ['Orders'],
        'summary': 'Retrieve all orders',
        'description': 'Fetch a list of all orders in the system.',
        'responses': {
            200: {
                'description': 'A list of orders',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            '_id': {'type': 'integer', 'example': 1},
                            'name': {'type': 'string', 'example': 'John Doe'},
                            'table': {'type': 'integer', 'example': 5},
                            'dishes': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'name': {'type': 'string', 'example': 'Pizza'},
                                        'price': {'type': 'number', 'example': 14.99},
                                        'quantity': {'type': 'integer', 'example': 2}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    })
    def get_orders(self):
        orders = self.order_service.get_all_orders()
        return jsonify(orders), 200

    @swag_from({
        'tags': ['Orders'],
        'summary': 'Create a new order',
        'description': 'Add a new order with a name, table number, and dishes.',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string', 'example': 'John Doe'},
                        'table': {'type': 'integer', 'example': 5},
                        'dishes': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'name': {'type': 'string', 'example': 'Pizza'},
                                    'price': {'type': 'number', 'example': 14.99},
                                    'quantity': {'type': 'integer', 'example': 2}
                                }
                            }
                        }
                    },
                    'required': ['name', 'table', 'dishes']
                }
            }
        ],
        'responses': {
            201: {'description': 'Order successfully created'},
            400: {'description': 'Invalid data'},
            500: {'description': 'Internal server error'}
        }
    })
    def add_order(self):
        try:
            request_data = request.json
            if not request_data:
                return jsonify({'error': 'Invalid data'}), 400

            name = request_data.get('name')
            table = request_data.get('table')
            dishes = request_data.get('dishes')

            # Validate fields
            try:
                self.order_schema.validate_name(name)
                self.order_schema.validate_table(table)
                self.order_schema.validate_dishes(dishes)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data: {e}'}), 400

            new_order = {
                'name': name,
                'table': table,
                'dishes': dishes,
                'status':"pending"
                
            }

            created_order = self.order_service.add_order(new_order)
            self.logger.info(f'New Order Created: {created_order}')
            return jsonify(created_order), 201
        except Exception as e:
            self.logger.error(f'Error adding new order to the database: {e}')
            return jsonify({'error': f'An exception has occurred: {e}'}), 500

    @swag_from({
        'tags': ['Orders'],
        'summary': 'Update an existing order',
        'description': 'Modify the details of an order by its ID.',
        'parameters': [
            {
                'name': 'order_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'example': 1,
                'description': 'The ID of the order to update'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string', 'example': 'John Doe'},
                        'table': {'type': 'integer', 'example': 5},
                        'dishes': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'name': {'type': 'string', 'example': 'Pizza'},
                                    'price': {'type': 'number', 'example': 14.99},
                                    'quantity': {'type': 'integer', 'example': 2}
                                }
                            }
                        }
                    },
                    'required': ['name', 'table', 'dishes']
                }
            }
        ],
        'responses': {
            200: {'description': 'Order successfully updated'},
            400: {'description': 'Invalid data'},
            404: {'description': 'Order not found'},
            500: {'description': 'Internal server error'}
        }
    })
    def update_order(self, order_id):
        try:
            request_data = request.json
            if not request_data:
                return jsonify({'error': 'Invalid data'}), 400

            name = request_data.get('name')
            table = request_data.get('table')
            dishes = request_data.get('dishes')

            # Validate fields
            try:
                self.order_schema.validate_name(name)
                self.order_schema.validate_table(table)
                self.order_schema.validate_dishes(dishes)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data: {e}'}), 400

            update_order = {
                '_id': order_id,
                'name': name,
                'table': table,
                'dishes': dishes,
                
            }

            updated_order = self.order_service.update_order(order_id, update_order)
            if updated_order:
                return jsonify(update_order), 200
            else:
                return jsonify({'error': 'Order not found'}), 404
        except Exception as e:
            self.logger.error(f'Error updating the order in the database: {e}')
            return jsonify({'error': f'An exception has occurred: {e}'}), 500

    @swag_from({
        'tags': ['Orders'],
        'summary': 'Delete an order',
        'description': 'Remove an order by its ID.',
        'parameters': [
            {
                'name': 'order_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'example': 1,
                'description': 'The ID of the order to delete'
            }
        ],
        'responses': {
            200: {'description': 'Order successfully deleted'},
            404: {'description': 'Order not found'},
            500: {'description': 'Internal server error'}
        }
    })
    def delete_order(self, order_id):
        try:
            deleted_order = self.order_service.delete_order(order_id)
            if deleted_order:
                return jsonify(deleted_order), 200
            else:
                return jsonify({'error': 'Order not found'}), 404
        except Exception as e:
            self.logger.error(f'Error deleting the order data: {e}')
            return jsonify({'error': f'Error deleting the order data: {e}'}), 500

    @swag_from({
        'tags': ['Health'],
        'summary': 'Health check',
        'description': 'Verify the service is up and running.',
        'responses': {
            200: {'description': 'Service is running'}
        }
    })
    def healthcheck(self):
        return jsonify({'status': 'up'}), 200
