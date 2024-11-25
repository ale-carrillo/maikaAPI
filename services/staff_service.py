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

if __name__ == '__main__':
    from models.staff_model import StaffModel

    logger = Logger()
    db_conn = StaffModel()
    staff_service = StaffService(db_conn)

    try:
        db_conn.connect_to_database()
        staff = staff_service.get_all_employees()
        logger.info(f'Staff fetched: {staff}')

        # Add employee
        new_employee = staff_service.add_employee({
            'name': 'John Doe',
            'title': 'Manager',
            'email': 'john.doe@example.com',
            'salary': 75000.0,
            'birthday': '1985-06-15',
            'status': True,
            'avatar': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAA...'
        })
        logger.info(f'New employee added: {new_employee}')

        # Fetch all employees
        staff = staff_service.get_all_employees()
        logger.info(f'Employees fetched: {staff}')

        # Get employee by ID
        employee = staff_service.get_employee_by_id(1)
        logger.info(f'Employee fetched: {employee}')

        # Update employee
        updated_employee = staff_service.update_employee(1, {
            'name': 'John Doe Updated',
            'title': 'Senior Manager',
            'email': 'john.doe.updated@example.com',
            'salary': 80000.0,
            'birthday': '1985-06-15',
            'status': False,  # Updated status
            'avatar': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAA...'  # Updated avatar
        })
        logger.info(f'Employee updated: {updated_employee}')

        staff = staff_service.get_all_employees()
        logger.info(f'Staff fetched: {staff}')

        # Delete employee by ID
        employee = staff_service.delete_employee(1)
        logger.info(f'employee deleted: {employee}')
    except Exception as e:
        logger.error(f'An error has ocurred: {e}')
    finally:
        db_conn.close_connection()
        logger.info('Connection to database was succesfully closed.')