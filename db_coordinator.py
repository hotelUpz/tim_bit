# from utils import UTILS
from log import log_exceptions_decorator
import mysql.connector
import time
import random 
import ast

class DB_COOORDINATOR():
    def __init__(self, host, port, user, password, database) -> None:
        # super().__init__()
        self.host, self.port, self.user, self.password, self.database = host, port, user, password, database

    @log_exceptions_decorator
    def db_connector(self):
        config = {
            'user': self.user,
            'password': self.password,            
            'host': 'localhost',
            # 'host': self.host,
            # 'port': self.port,
            'database': self.database,
        }
        for _ in range(2):
            try:
                self.connection = mysql.connector.connect(**config)      
                print("Writerr connection established")
                self.cursor = self.connection.cursor()
                return True
            except Exception as e:
                print(f"Error connecting to MySQL: {e}")
                time.sleep(random.randrange(1,4))                
        return False
        
    def read_db_data(self):
        records = []
        try:
            self.cursor.execute("SELECT * FROM DB_BITGET_COORDINSTOR_LISTING_DATA")
            records = self.cursor.fetchall()
        except Exception as ex:
            print(ex)
            return
        finally:
            self.connection.close()
            return records

    def formate_db_data(self, db_reading_data):
        try:            
            return db_reading_data[0][1], ast.literal_eval(db_reading_data[0][2])
        except Exception as ex:
            print(ex)
        return {}, None

            

