from flask import jsonify
from logger.logger_base import Logger

class OrderService:
    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn



    def get_all_orders(self):
        try:
            orders = list(self.db_conn.db.orders.find())
            return orders
        except Exception as e:
            self.logger.error(f'Error fetching all orders from the database: {e}')
            return jsonify({ 'error': f'Error fetching all orders from the database: {e}' }), 500
        
      
    
    def add_order(self, new_order):
        try:

            last_order = self.db_conn.db.orders.find_one(sort=[('_id', -1)])
            next_id = (last_order['_id'] + 1 if last_order else 1)
            new_order["_id"] = next_id
            
            self.db_conn.db.orders.insert_one(new_order)
            return new_order
        except Exception as e:
            self.logger.error(f'Error creating the new order: {e}')
            return jsonify({ 'error': f'Error creating the new order: {e}' }), 500
        



    def get_order_by_id(self, order_id):
        try:
            order = self.db_conn.db.orders.find_one({'_id': order_id})
            return order
        except Exception as e:
            self.logger.error(f'Error fetching the order by id from the database: {e}')
            return jsonify({'error': f'Error fetching the order by id from the database: {e}'}), 500
        
    def update_order(self, order_id, order):
        try:
            update_order = self.get_order_by_id(order_id)  

            if update_order:
                updated_order = self.db_conn.db.orders.update_one({'_id': order_id}, {'$set': order})  
                if updated_order.modified_count > 0:  
                    return updated_order
                else:
                    return 'The order is already up-to-date'
            else:
                return None
        except Exception as e:
            self.logger.error(f'Error updating the order: {e}')
            return jsonify({'error': f'Error updating the order: {e}'}), 500
        
    def delete_order(self, order_id):
        try:
            deleted_order = self.get_order_by_id(order_id)

            if deleted_order:
                self.db_conn.db.orders.delete_one({'_id': order_id})
                return deleted_order
            else:
                return None
        except Exception as e:
            self.logger.error(f'Error deleting the order: {e}')
            return jsonify({'error': f'Error deleting the order: {e}'}), 500


print('hoadal')
if __name__ == '__main__':
    from models.order_model import OrderModel

    logger = Logger()
    db_conn = OrderModel()
    order_service = OrderService(db_conn)

    try:
        db_conn.connect_to_database()
        orders = order_service.get_all_orders()
        print(f'Orders fetched: {orders}')
        logger.info(f'Orders fetched: {orders}')

        # Add order
        new_order = order_service.add_order({
            'name': 'O1',
            'table': 1,
            'dishes': [
                {'name': 'Pizza', 'price': 15.99, 'quantity': 2},
                {'name': 'Pasta', 'price': 12.50, 'quantity': 771}
            ]
        })
        logger.info(f'New order added: {new_order}')


        # Get order by ID
        order = order_service.get_order_by_id(3)
        logger.info(f'Order fetched by ID: {order}')
    except Exception as e:
        logger.error(f'An error has occurred: {e}')
    finally:
        db_conn.close_connection()
        logger.info('Connection to database was successfully closed.')
