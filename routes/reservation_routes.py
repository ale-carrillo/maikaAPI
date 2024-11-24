from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from logger.logger_base import Logger
from flasgger import swag_from

class ReservationRoute(Blueprint):
    def __init__(self, reservation_service, reservation_schema):
        super().__init__('reservation', __name__)
        self.reservation_service = reservation_service
        self.reservation_schema = reservation_schema
        self.register_routes()
        self.logger = Logger()

    # Register the API endpoints with corresponding methods
    def register_routes(self):
        self.route('/api/v1/reservations', methods=['GET'])(self.get_reservations)
        self.route('/api/v1/reservations', methods=['POST'])(self.add_reservation)
        self.route('/api/v1/reservations/<int:reservation_id>', methods = ['PUT'])(self.update_reservation)
        self.route('/api/v1/reservations/<int:reservation_id>', methods = ['DELETE'])(self.delete_reservation)
        self.route('/healthcheck', methods=['GET'])(self.healthcheck)
    
    @swag_from({
        'tags': ['Reservations'],
        'responses': {
            200: {
                'description': 'Get All Reservations',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'date': {'type': 'string'},
                            'people': {'type': 'integer'},
                            't_reservation': {'type': 'string'},
                            'name': {'type': 'string'},
                            'last_name': {'type': 'string'},
                            'phone': {'type': 'integer'},
                            'email': {'type': 'string'},
                            'special': {'type': 'string'}
                        }
                    }
                }
            }
        }
    })
    def get_reservations(self):
    # Fetches all reservations from the reservation service
        reservations = self.reservation_service.get_all_reservations()
        return jsonify(reservations), 200
    
    @swag_from({
        'tags': ['Reservations'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'date': {'type': 'string'},
                        'people': {'type': 'integer'},
                        't_reservation': {'type': 'string'},
                        'name': {'type': 'string'},
                        'last_name': {'type': 'string'},
                        'phone': {'type': 'integer'},
                        'email': {'type': 'string'},
                        'special': {'type': 'string'}
                    },
                    'required': ['date', 'people', 't_reservation', 'name', 'last_name', 'phone', 'email']
                }
            }
        ],
        'responses': {
            201: {
                'description': 'Reservation successfully created'
            },
            400: {
                'description': 'Invalid data'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    def add_reservation(self):
    # Create a new reservation
        try:
            request_data = request.json

            if not request_data:
                return jsonify({'error': 'invalid data'}), 400
            
            date = request_data.get('date')
            people = request_data.get('people')
            t_reservation = request_data.get('t_reservation')
            name = request_data.get('name')
            last_name = request_data.get('last_name')
            phone = request_data.get('phone')
            email = request_data.get('email')
            special = request_data.get('special', '')


            try:
                self.reservation_schema.validate_date(date)
                self.reservation_schema.validate_people(people)
                self.reservation_schema.validate_t_reservation(t_reservation)
                self.reservation_schema.validate_name(name)
                self.reservation_schema.validate_last_name(last_name)
                self.reservation_schema.validate_phone(phone)
                self.reservation_schema.validate_email(email)
                if special:
                    self.reservation_schema.validate_special(special)
            except ValidationError as e:
                return jsonify({ 'error': 'Invalid data' }), 400

            new_reservation = {
                'date': date,
                'people': people,
                't_reservation': t_reservation,
                'name': name,
                'last_name': last_name,
                'phone': phone,
                'email': email,
                'special': special
            }

            created_reservation = self.reservation_service.add_reservation(new_reservation)
            return jsonify(created_reservation), 201
        except Exception as e:
            self.logger.error(f'Error adding new Reservation to the database: {e}')
            return jsonify({ 'error': f'An exception has ocurred: {e}' }), 500
    
    @swag_from({
        'tags': ['Reservations'],
        'parameters': [
            {
                'name': 'reservation_id',
                'in': 'path',
                'required': True,
                'type': 'string',
                'description': 'ID of the Reservation to update'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'date': {'type': 'string', 'example': '21 Nov 2024 14:30'},
                        'people': {'type': 'integer'},
                        't_reservation': {'type': 'string'},
                        'name': {'type': 'string'},
                        'last_name': {'type': 'string'},
                        'phone': {'type': 'integer'},
                        'email': {'type': 'string'},
                        'special': {'type': 'string'}
                    },
                    'required': ['date', 'people', 't_reservation', 'name', 'last_name', 'phone', 'email']
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Reservation successfully updated',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'date': {'type': 'string', 'example': '21 Nov 2024 14:30'},
                        'people': {'type': 'integer'},
                        't_reservation': {'type': 'string'},
                        'name': {'type': 'string'},
                        'last_name': {'type': 'string'},
                        'phone': {'type': 'integer'},
                        'email': {'type': 'string'},
                        'special': {'type': 'string'}
                    }
                }
            },
            400: {
                'description': 'Invalid data'
            },
            404: {
                'description': 'Reservation not found'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    def update_reservation(self, reservation_id):
    # Update the reservation data
        try:
            request_data = request.json    
            
            if not request_data:
                return jsonify({'error': 'Invalid data'}), 400
            
            date = request_data.get('date')
            people = request_data.get('people')
            t_reservation = request_data.get('t_reservation')
            name = request_data.get('name')
            last_name = request_data.get('last_name')
            phone = request_data.get('phone')
            email = request_data.get('email')
            special = request_data.get('special', '')        

            try:
                self.reservation_schema.validate_date(date)
                self.reservation_schema.validate_people(people)
                self.reservation_schema.validate_t_reservation(t_reservation)
                self.reservation_schema.validate_name(name)
                self.reservation_schema.validate_last_name(last_name)
                self.reservation_schema.validate_phone(phone)
                self.reservation_schema.validate_email(email)
                self.reservation_schema.validate_special(special)
            except ValidationError as e:
                return jsonify({'error': f'Invalid data {e}'}), 400
            
            update_reservation = {
                '_id': reservation_id,
                'date': date,
                'people': people,
                't_reservation': t_reservation,
                'name': name,
                'last_name': last_name,
                'phone': phone,
                'email': email,
                'special': special
            }
            updated_reservation = self.reservation_service.update_reservation(reservation_id, update_reservation)
            if updated_reservation:
                return jsonify(update_reservation), 200
            else:            
                return jsonify({'error': 'Reservation not found'}), 404
        except Exception as e:
            self.logger.error(f'Error updating the Reservation in the database: {e}')
            return jsonify({'error': f'An exception has ocurred: {e}'})
    
    @swag_from({
        'tags': ['Reservations'],
        'parameters': [
            {
                'name': 'reservation_id',
                'in': 'path',
                'required': True,
                'type': 'string',
                'description': 'ID of the Reservation to delete'
            }
        ],
        'responses': {
            200: {
                'description': 'Reservation successfully deleted'
            },
            404: {
                'description': 'Reservation not found'
            },
            500: {
                'description': 'Internal server error'
            }
        }
    })
    def delete_reservation(self, reservation_id):
    # Delete a reservation
        try:
            delete_reservation = self.reservation_service.delete_reservation(reservation_id)

            if delete_reservation:
                return jsonify(delete_reservation), 200
            else:
                jsonify({'error': 'Reservation not found'}), 404
        except Exception as e:
            self.logger.error(f'Error deleting the Reservation data: {e}')
            jsonify({'error': f'Error deleting the Reservation data: {e}'}), 500

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
    def healthcheck(self):
    # Healhthcheck endpoint
        return jsonify({ 'status': 'up' }), 200