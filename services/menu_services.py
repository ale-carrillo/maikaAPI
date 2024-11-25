from flask import jsonify
from logger.logger_base import Logger

class MenuService:
    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn

    def get_all_meals(self):
        try:
            meals = list(self.db_conn.db.menu.find())
            return meals
        except Exception as e:
            self.logger.error(f'Error fetching all meals from the database: {e}')
            return jsonify({ 'error': f'Error fetching all meals from the database: {e}' }), 500
        
    def add_meal(self, new_meal):
        try:
            last_meal = self.db_conn.db.menu.find_one(sort=[('_id', -1)])
            next_id = (last_meal['_id'] + 1 if last_meal else 1)
            new_meal["_id"] = next_id
            self.db_conn.db.menu.insert_one(new_meal)
            return new_meal
        except Exception as e:
            self.logger.error(f'Error creating the new meal: {e}')
            return jsonify({ 'error': f'Error creating the new meal: {e}' }), 500

if __name__ == '__main__':
    from models.menu_model import MenuModel

    logger = Logger()
    db_conn = MenuModel()
    menbu_service = MenuService(db_conn)

    try:
        db_conn.connect_to_database()
        meals = menbu_service.get_all_meals()
        print(f'POrueba de platillos: {meals}')
        logger.info(f'POrueba de platillos: {meals}')

        new_meal = menbu_service.add_meal({'meal': 'Pasta', 'description': 'Pasta is a type of food made from a mixture of flour'})
        logger.info(f'New meal added: {new_meal}')


    except Exception as e:
        logger.error(f'An error has ocurred: {e}')
    finally:
        db_conn.close_connection()
        logger.info('Connection to database was succesfully closed.')
