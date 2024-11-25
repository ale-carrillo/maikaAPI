from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from logger.logger_base import Logger
from flasgger import swag_from

class StaffRoutes(Blueprint):
    def __init__(self, staff_service, staff_schema):
        super().__init__('staff', __name__)
        self.staff_service = staff_service
        self.staff_schema = staff_schema
        self.register_routes()
        self.logger = Logger()

    def register_routes(self):
        self.route('/api/v1/staff', methods=['GET'])(self.get_staff)
        self.route('/api/v1/staff', methods=['POST'])(self.add_employee)
        self.route('/api/v1/staff/<int:employee_id>', methods=['PUT'])(self.update_employee)
        self.route('/api/v1/staff/<int:employee_id>', methods=['DELETE'])(self.delete_employee)
        self.route('/healthcheck', methods=['GET'])(self.healthcheck)

    @swag_from({
        'tags': ['Staff'],
        'responses': {
            200: {
                'description': 'Get all employees',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'name': {'type': 'string'},
                            'title': {'type': 'string'},
                            'email': {'type': 'string'},
                            'salary': {'type': 'number'},
                            'birthday': {'type': 'string'},
                            'status': {'type': 'boolean'},
                            'avatar': {'type': 'string'}
                        }
                    }
                }
            }
        }
    })
    def get_staff(self):
        try:
            staff = self.staff_service.get_all_employees()
            return jsonify(staff), 200
        except Exception as e:
            self.logger.error(f'Error fetching employees: {e}')
            return jsonify({'error': 'Internal server error'}), 500

    @swag_from({
        'tags': ['Staff'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string'},
                        'title': {'type': 'string'},
                        'email': {'type': 'string'},
                        'salary': {'type': 'number'},
                        'birthday': {'type': 'string'},
                        'status': {'type': 'boolean'},
                        'avatar': {'type': 'string'}
                    },
                    'required': ['name', 'title', 'email', 'salary', 'birthday', 'status', 'avatar']
                }
            }
        ],
        'responses': {
            201: {'description': 'Employee successfully created'},
            400: {'description': 'Invalid data'},
            500: {'description': 'Internal server error'}
        }
    })
    def add_employee(self):
        try:
            request_data = request.json

            if not request_data:
                return jsonify({'error': 'Invalid data'}), 400

            name = request_data.get('name')
            title = request_data.get('title')
            salary = request_data.get('salary')
            avatar = request_data.get('avatar')
            status = request_data.get('status')
            email = request_data.get('email')
            birthday = request_data.get('birthday')

            try:
                self.staff_schema.validate_name(name)
                self.staff_schema.validate_avatar(avatar)
                self.staff_schema.validate_salary(salary)
                self.staff_schema.validate_birthday(birthday)
                self.staff_schema.validate_email(email)
                self.staff_schema.validate_status(status)
                self.staff_schema.validate_title(title)

                
            except ValidationError as e:
                return jsonify({'error': e.messages}), 400

            new_employee = {
                'name': name,
                'avatar': avatar,
                'salary': salary,
                'title': title,
                'birthday': birthday,
                'status': status,
                'email': email
            }

            created_employee = self.staff_service.add_employee(new_employee)
            return jsonify(created_employee), 201
        except Exception as e:
            self.logger.error(f'Error adding new employee: {e}')
            return jsonify({'error': 'Internal server error'}), 500

    @swag_from({
        'tags': ['Staff'],
        'parameters': [
            {
                'name': 'employee_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID of the employee to update'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string'},
                        'title': {'type': 'string'},
                        'email': {'type': 'string'},
                        'salary': {'type': 'number'},
                        'birthday': {'type': 'string'},
                        'status': {'type': 'boolean'},
                        'avatar': {'type': 'string'}
                    }
                }
            }
        ],
        'responses': {
            200: {'description': 'Employee successfully updated'},
            400: {'description': 'Invalid data'},
            404: {'description': 'Employee not found'},
            500: {'description': 'Internal server error'}
        }
    })
    def update_employee(self, employee_id):
        try:
            request_data = request.json

            if not request_data:
                return jsonify({'error': 'Invalid data'}), 400

            name = request_data.get('name')
            title = request_data.get('title')
            salary = request_data.get('salary')
            avatar = request_data.get('avatar')
            status = request_data.get('status')
            email = request_data.get('email')
            birthday = request_data.get('birthday')

            try:
                self.staff_schema.validate_name(name)
                self.staff_schema.validate_avatar(avatar)
                self.staff_schema.validate_salary(salary)
                self.staff_schema.validate_birthday(birthday)
                self.staff_schema.validate_email(email)
                self.staff_schema.validate_status(status)
                self.staff_schema.validate_title(title)

            except ValidationError as e:
                return jsonify({'error': e.messages}), 400

            update_employee = {
                '_id':employee_id,
                'name': name,
                'avatar': avatar,
                'salary': salary,
                'title': title,
                'birthday': birthday,
                'status': status,
                'email': email
            }

            updated_employee = self.staff_service.update_employee(employee_id,update_employee)

            if not updated_employee:
                return jsonify({'error': 'Employee not found'}), 404

            return jsonify(updated_employee), 200
        except Exception as e:
            self.logger.error(f'Error updating employee: {e}')
            return jsonify({'error': 'Internal server error'}), 500

    @swag_from({
        'tags': ['Staff'],
        'parameters': [
            {
                'name': 'employee_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'ID of the employee to delete'
            }
        ],
        'responses': {
            200: {'description': 'Employee successfully deleted'},
            404: {'description': 'Employee not found'},
            500: {'description': 'Internal server error'}
        }
    })
    def delete_employee(self, employee_id):
        try:
            deleted = self.staff_service.delete_employee(employee_id)
            if not deleted:
                return jsonify({'error': 'Employee not found'}), 404
            return jsonify({'message': 'Employee successfully deleted'}), 200
        except Exception as e:
            self.logger.error(f'Error deleting employee: {e}')
            return jsonify({'error': 'Internal server error'}), 500

    @swag_from({
        'tags': ['Health'],
        'responses': {
            200: {'description': 'Service is up and running'},
            500: {'description': 'Internal server error'}
        }
    })
    def healthcheck(self):
        return jsonify({'status': 'up'}), 200
