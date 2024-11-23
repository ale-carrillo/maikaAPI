from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from logger.logger_base import Logger
from flasgger import swag_from

class PaymentRoutes(Blueprint):
    def _init_(self, payment_service, payment_schema):
        super()._init('payment', __name__)
        self.payment_service = payment_service
        self.payment_schema = payment_schema
        self.register_routes()
        self.logger = Logger()

    def register_routes(self):
        self.route('/api/v1/payments/pending', methods=['GET'])(self.get_all_orders_to_pay)
        self.route('/api/v1/payments', methods=['GET'])(self.get_all_payments)
        self.route('/api/v1/payments', methods=['POST'])(self.add_payment)
        self.route('/api/v1/payments/<payment_id>', methods=['DELETE'])(self.delete_payment)

    @swag_from({
        'tags': ['Payments'],
        'summary': 'Get all pending orders to pay',
        'responses': {
            200: {
                'description': 'List of all pending orders',
                'content': {
                    'application/json': {
                        'example': [{'order_id': 1, 'total': 1500}]
                    }
                }
            }
        }
    })
    def get_all_orders_to_pay(self):
        orders = self.payment_service.get_all_orders_to_pay()
        return jsonify(orders), 200

    @swag_from({
        'tags': ['Payments'],
        'summary': 'Get all payments',
        'responses': {
            200: {
                'description': 'List of all payments',
                'content': {
                    'application/json': {
                        'example': [{'payment_id': 1, 'amount': 500}]
                    }
                }
            }
        }
    })
    def get_all_payments(self):
        orders = self.payment_service.get_all_payments()
        return jsonify(orders), 200

    @swag_from({
        'tags': ['Payments'],
        'summary': 'Add a new payment',
        'parameters': [
    {
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
                'rfc': {'type': 'string'},
                'payment_type': {'type': 'string'},
                'table': {'type': 'integer'},
                'items': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'name': {'type': 'string'},
                            'quantity': {'type': 'integer'},
                            'price': {'type': 'number'}
                        },
                        'required': ['name', 'quantity', 'price']
                    }
                }
            },
            'required': ['name', 'rfc', 'payment_type', 'table', 'items']
        }
    }
],

        'responses': {
            201: {
                'description': 'Payment created successfully',
                'content': {
                    'application/json': {
                        'example': {'payment_id': 1, 'total': 650}
                    }
                }
            },
            400: {
                'description': 'Invalid data',
                'content': {
                    'application/json': {
                        'example': {'error': 'Invalid data: name is required'}
                    }
                }
            },
            500: {
                'description': 'Server error',
                'content': {
                    'application/json': {
                        'example': {'error': 'An error occurred: Database unreachable'}
                    }
                }
            }
        }
    })
    def add_payment(self):
        try:
            request_data = request.json
            if not request_data:
                return jsonify({'error': 'Invalid data'}), 400

            name = request_data.get('name')
            rfc = request_data.get('rfc')
            payment_type = request_data.get('payment_type')
            table = request_data.get('table')
            items = request_data.get('items')

            try:
                self.payment_schema.validate_name(name)
                self.payment_schema.validate_rfc(rfc)
                self.payment_schema.validate_payment_type(payment_type)
                self.payment_schema.validate_table(table)
                self.payment_schema.validate_items(items)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data: {e}'}), 400

            new_payment = {
                'name': name,
                'table': table,
                'items': items,
                'rfc': rfc,
                'payment_type': payment_type
            }

            created_payment = self.payment_service.add_payment(new_payment)
            self.logger.info(f'New Payment Created: {created_payment}')
            return jsonify(created_payment), 201

        except Exception as e:
            self.logger.error(f'Error adding a new payment: {e}')
            return jsonify({'error': f'An error occurred: {e}'}), 500

    @swag_from({
        'tags': ['Payments'],
        'summary': 'Delete a payment',
        'parameters': [
            {
                'name': 'payment_id',
                'in': 'path',
                'required': True,
                'schema': {'type': 'integer'},
                'description': 'The ID of the payment to delete'
            }
        ],
        'responses': {
            200: {
                'description': 'Payment deleted successfully',
                'content': {
                    'application/json': {
                        'example': {'message': 'Payment deleted successfully'}
                    }
                }
            },
            404: {
                'description': 'Payment not found',
                'content': {
                    'application/json': {
                        'example': {'error': 'Payment not found'}
                    }
                }
            },
            500: {
                'description': 'Server error',
                'content': {
                    'application/json': {
                        'example': {'error': 'Error deleting the payment'}
                    }
                }
            }
        }
    })
    def delete_payment(self, payment_id):
        try:
            delete_payment = self.payment_service.delete_payment(payment_id)
            if delete_payment:
                return jsonify(delete_payment), 200
            else:
                return jsonify({'error': 'Payment not found'}), 404
        except Exception as e:
            self.logger.error(f'Error deleting the payment data: {e}')
            return jsonify({'error': f'Error deleting the payment data: {e}'}), 500