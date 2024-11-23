from flask import jsonify
from logger.logger_base import Logger

class PaymentService:
    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn

    def calculate_total_price(self, items):
        """
        Calcula el precio total de los ítems en la orden.
        """
        try:
            total_price = 0
            for item in items:
                total_price += item['price'] * item['quantity']
            return total_price
        except Exception as e:
            self.logger.error(f"Error calculating total price: {e}")
            raise

    def get_all_payments(self):
        """
        Obtiene todas las órdenes almacenadas en la base de datos.
        """
        try:
            payments = list(self.db_conn.db.payments.find())
            return payments
        except Exception as e:
            self.logger.error(f'Error fetching all payments from the database: {e}')
            return jsonify({'error': f'Error fetching all payments from the database: {e}'}), 500

    def add_payment(self, new_payment):
        """
        Añade un nuevo pago a la base de datos.
        """
        try:
            items = new_payment.get('items', [])
            total_price = self.calculate_total_price(items)
            new_payment['total_price'] = total_price
            
            result = self.db_conn.db.payments.insert_one(new_payment)
            new_payment['_id'] = result.inserted_id
            return new_payment
        except Exception as e:
            self.logger.error(f'Error creating the new payment: {e}')
            return jsonify({'error': f'Error creating the new payment: {e}'}), 500

    def get_payment_by_id(self, payment_id):
        """
        Obtiene un pago por su ID.
        """
        try:
            payment = self.db_conn.db.payments.find_one({'_id': payment_id})
            return payment
        except Exception as e:
            self.logger.error(f'Error fetching the payment by id from the database: {e}')
            return jsonify({'error': f'Error fetching the payment by id from the database: {e}'}), 500

    def update_payment(self, payment_id, payment_data):
        """
        Actualiza un pago existente.
        """
        try:
            existing_payment = self.get_payment_by_id(payment_id)

            if existing_payment:
                updated_payment = self.db_conn.db.payments.update_one(
                    {'_id': payment_id},
                    {'$set': payment_data}
                )
                if updated_payment.modified_count > 0:
                    return payment_data
                else:
                    return 'The payment is already up-to-date'
            else:
                return None
        except Exception as e:
            self.logger.error(f'Error updating the payment: {e}')
            return jsonify({'error': f'Error updating the payment: {e}'}), 500

    def delete_payment(self, payment_id):
        """
        Elimina un pago por su ID.
        """
        try:
            existing_payment = self.get_payment_by_id(payment_id)

            if existing_payment:
                self.db_conn.db.payments.delete_one({'_id': payment_id})
                return existing_payment
            else:
                return None
        except Exception as e:
            self.logger.error(f'Error deleting the payment: {e}')
            return jsonify({'error': f'Error deleting the payment: {e}'}), 500


if __name__ == '__main__':
    from models.payment_model import PaymentModel

    logger = Logger()
    db_conn = PaymentModel()
    payment_service = PaymentService(db_conn)

    try:
        db_conn.connect_to_database()
        
        # Obtener todos los pagos
        payments = payment_service.get_all_payments()
        logger.info(f'Payments fetched: {payments}')

        # Añadir un nuevo pago
        new_payment = payment_service.add_payment({
            'name': 'Payment1',
            'user_id': 1,
            'items': [
                {'dish': 'Burger', 'price': 10.99, 'quantity': 2},
                {'dish': 'Fries', 'price': 3.50, 'quantity': 1}
            ]
        })
        logger.info(f'New payment added: {new_payment}')

        # Obtener un pago por ID
        payment = payment_service.get_payment_by_id(new_payment['_id'])
        logger.info(f'Payment fetched by ID: {payment}')

    except Exception as e:
        logger.error(f'An error has occurred: {e}')
    finally:
        db_conn.close_connection()
        logger.info('Connection to database was successfully closed.')
