from flask import jsonify
from logger.logger_base import Logger

class PaymentService:
    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn

    def get_all_orders_to_pay(self):
        try:
            orders = list(self.db_conn.db.orders.find())
            for order in orders:
                total = 0
                for dish in order["dishes"]:
                    total += dish["price"] * dish["quantity"]
                order["total"] = total
            return orders
        except Exception as e:
            self.logger.error(f'Error fetching all orders to pay from the database: {e}')
            return jsonify({'error': f'Error fetching all orders to pay from the database: {e}'}), 500

    def get_all_payments(self):
        """
        Obtiene todas las órdenes almacenadas en la base de datos.
        """
        try:
            payments = list(self.db_conn.db.payments.find({"active": True}))
            return payments
        except Exception as e:
            self.logger.error(f'Error fetching all payments from the database: {e}')
            return jsonify({'error': f'Error fetching all payments from the database: {e}'}), 500

    def add_payment(self, new_payment):
        """
        Añade un nuevo pago a la base de datos.
        """
        try:
            self.logger.info("INICIO")
            self.logger.info(new_payment["order_id"])
            self.logger.info("INICIO 2")
            last_book = self.db_conn.db.payments.find_one(sort=[('_id', -1)])
            next_id = (last_book['_id'] + 1 if last_book else 1)
            new_payment['_id'] = next_id
            new_payment['active'] = True
            self.db_conn.db.payments.insert_one(new_payment)
            self.db_conn.db.orders.delete_one({'_id': new_payment['order_id']})    
            return new_payment
        except Exception as e:
            self.logger.error(f'Error creating the new payment: {e}')
            return jsonify({'error': f'Error creating the new payment: {e}'}), 500

    def get_payment_by_id(self, payment_id):
        """
        Obtiene un pago por su ID.
        """
        try:
            payment_id =int(payment_id)
            self.logger.info(type(payment_id))
            payment = self.db_conn.db.payments.find_one({'_id': payment_id})
            self.logger.info(payment)
            return payment
        except Exception as e:
            self.logger.error(f'Error fetching the payment by id from the database: {e}')
            return jsonify({'error': f'Error fetching the payment by id from the database: {e}'}), 500

    def delete_payment(self, payment_id):
        """
        Elimina un pago por su ID.
        """
        try:
            payment_id = int(payment_id)
            existing_payment = self.get_payment_by_id(payment_id)

            if existing_payment:
                if existing_payment["active"]:
                    result = self.db_conn.db.payments.update_one({'_id': payment_id}, {'$set': {"active": False}})    #Libro actualizado
                    if result.modified_count > 0: 
                            existing_payment["active"] = False
                            return existing_payment
                    else:
                        return None
                else:
                    return None
            else:
                return None
        except Exception as e:
            self.logger.error(f'Error deleting the payment: {e}')
            return jsonify({'error': f'Error deleting the payment: {e}'}), 500


