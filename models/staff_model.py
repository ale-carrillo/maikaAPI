import os
from logger.logger_base import Logger
from pymongo import MongoClient


class StaffModel:
    def __init__(self):
        self.client = None
        self.db=None
        self.logger=Logger()

    def connect_to_database(self):
        mongodb_user = os.environ.get('MONGODB_USER')
        mongodb_pass = os.environ.get('MONGODB_PASS')
        mongodb_host = os.environ.get('MONGODB_HOST')

        if not mongodb_user or not mongodb_pass or not mongodb_host:
            self.logger.critical('MongoDB environment variables are required nut mis')
            raise ValueError('Set enviroment variables: MONGODB_USER,MONGODB_PASS,MONGODB_HOST')
        try:
            self.client = MongoClient(
                host = mongodb_host,
                port = 27017,
                username = mongodb_user,
                password = mongodb_pass,
                authSource = 'admin',
                authMechanism = 'SCRAM-SHA-256',
                serverSelectionTimeOutMs =5000
            )
            self.db = self.client['microservices']
            if self.db.list_collection_names():
                self.logger.info('Connected to MOngoDB database succesfully')
        except Exception as e:
            self.logger.critical(f'Failed to connect to database: {e}')
            raise
    
    def close_connection(self):
        if self.client:
            self.client.close()

if __name__=='__main__':
    db_conn = StaffModel()
    logger = Logger()


    try:
        db_conn.connect_to_database()
    except Exception as e:
        logger.critical(f'An error ocurred {e}')
    finally:
        db_conn.close_connection()
        logger.info('COnnection to the database was succesfully closed')

        
