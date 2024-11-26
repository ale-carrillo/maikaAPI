from flask import jsonify
from logger.logger_base import Logger

class StaffService:
    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn

    def get_all_employees(self):
        try:
            staff = list(self.db_conn.db.staff.find())
            return staff
        except Exception as e:
            self.logger.error(f'Error fetching staff from the database: {e}')
            return jsonify({ 'error': f'Error fetching staff from the database: {e}' }), 500
        
    def add_employee(self, new_employee):
        try:
            last_employee = self.db_conn.db.staff.find_one(sort=[('_id', -1)])
            next_id = (last_employee['_id'] + 1 if last_employee else 1)
            new_employee["_id"] = next_id
            self.db_conn.db.staff.insert_one(new_employee)
            return new_employee
        except Exception as e:
            return jsonify({'error': f'Error creating the new employee: {e}'}), 500
        
    def get_employee_by_id(self, employee_id):
        try:
            employee = self.db_conn.db.staff.find_one({'_id': employee_id})
            return employee
        except Exception as e:
            self.logger.error(f'Error fetching the employee id from the database: {e}')
            return jsonify({'error': f'Error fetching the employee id from the database: {e}'}), 500
        
    def update_employee(self, employee_id, employee):
        try:
            update_employee = self.get_employee_by_id(employee_id)

            if update_employee:
                updated_employee = self.db_conn.db.staff.update_one({'_id': employee_id}, {'$set': employee})
                if updated_employee.modified_count > 0:
                    return employee
                else:
                    return 'The employee is already up-to-date'
            else:
                return None
        except Exception as e:
            self.logger.error(f'Error updating the employee: {e}')
            return jsonify({'error': f'Error updating the employee: {e}'}), 500
        
    
        
    def delete_employee(self, employee_id):
        try:
            deleted_employee = self.get_employee_by_id(employee_id)

            if deleted_employee:
                self.db_conn.db.staff.delete_one({'_id': employee_id})            
                return deleted_employee
            else:
                return None            
        except Exception as e:
            self.logger.error(f'Error deleting the employee data: {e}')
            return jsonify({'error': f'Error deleting the employee: {e}'}), 500
