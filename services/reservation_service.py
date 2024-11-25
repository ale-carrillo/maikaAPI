from flask import jsonify
from logger.logger_base import Logger

class ReservationService:
    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn

    # Get all servervations
    def get_all_reservations(self):
        try:
            reservations = list(self.db_conn.db.reservations.find())
            return reservations
        except Exception as e:
            self.logger.error(f'Error fetching all reservations from the database: {e}')
            return jsonify({ 'error': f'Error fetching all reservations from the database: {e}' }), 500
    
    # New reservation
    def add_reservation(self, new_reservation):
        try:
            last_reservation = self.db_conn.db.reservations.find_one(sort=[('_id', -1)])
            next_id = (last_reservation['_id'] + 1 if last_reservation else 1)
            new_reservation["_id"] = next_id
            self.db_conn.db.reservations.insert_one(new_reservation)
            return new_reservation
        except Exception as e:
            self.logger.error(f'Error creating the new reservation: {e}')
            return jsonify({ 'error': f'Error creating the new reservation: {e}' }), 500
        
    # Get reservation by id
    def get_reservation_by_id(self, reservation_id):
        try:
            reservation = self.db_conn.db.reservations.find_one({'_id': reservation_id})
            return reservation
        except Exception as e:
            self.logger.error(f'Error fetching the reservation id from the database: {e}')
            return jsonify({'error': f'Error fetching the reservation id from the database: {e}'}), 500
        
    # Update a reservation by id
    def update_reservation(self, reservation_id, reservation):
        try:
            update_reservation = self.get_reservation_by_id(reservation_id)

            if update_reservation:
                updated_reservation = self.db_conn.db.reservations.update_one({'_id': reservation_id}, {'$set': reservation})
                if updated_reservation.modified_count > 0:
                    return reservation
                else:
                    return 'The reservation is already up-to-date'
            else:
                return None
        except Exception as e:
            self.logger.error(f'Error updating the reservation: {e}')
            return jsonify({'error': f'Error updating the reservation: {e}'}), 500
        
    # Delete a reservation by id
    def delete_reservation(self, reservation_id):
        try:
            deleted_reservation = self.get_reservation_by_id(reservation_id)

            if deleted_reservation:
                self.db_conn.db.reservations.delete_one({'_id': reservation_id})            
                return deleted_reservation
            else:
                return None            
        except Exception as e:
            self.logger.error(f'Error deleting the reservation data: {e}')
            return jsonify({'error': f'Error deleting the reservation: {e}'}), 500

if __name__ == '__main__':
    from models.reservation_model import reservationModel

    logger = Logger()
    db_conn = ReservationModel()
    reservation_service = ReservationService(db_conn)

    try:
        db_conn.connect_to_database()
        reservations = reservation_service.get_all_reservations()
        logger.info(f'reservations fetched: {reservations}')

        # Add reservation
        new_reservation = reservation_service.add_reservation(1, {
            'date': '22 Nov 2024 20:00',
            'people': '2',
            't_reservation': 'Romantic',
            'name': 'Anthony',
            'last_name': 'Sprouse',
            'phone': '1234567890',
            'email': 'ant@gmail.com',
            'special': 'Proposal'
        })
        logger.info(f'New reservation added: {new_reservation}')
        
        reservations = reservation_service.get_all_reservations()
        logger.info(f'reservations fetched: {reservations}')

        # Get reservation by ID
        reservation = reservation_service.get_reservation_by_id(1)
        logger.info(f'reservation fetched: {reservation}')

        # Update reservation
        new_reservation = reservation_service.update_reservation(1, {
            'date': '22 Nov 2024 20:00',
            'people': '2',
            't_reservation': 'Romantic',
            'name': 'Anthony',
            'last_name': 'Sprouse',
            'phone': '1234567890',
            'email': 'antony@gmail.com',
            'special': 'Proposal'
        })
        logger.info(f'reservation updated: {new_reservation}')
        
        reservations = reservation_service.get_all_reservations()
        logger.info(f'reservations fetched: {reservations}')

        # Delete reservation by ID
        reservation = reservation_service.delete_reservation(1)
        logger.info(f'reservation deleted: {reservation}')
    except Exception as e:
        logger.error(f'An error has ocurred: {e}')
    finally:
        db_conn.close_connection()
        logger.info('Connection to database was succesfully closed.')
