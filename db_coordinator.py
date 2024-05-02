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

    # @log_exceptions_decorator
    # def create_table(self):
    #     self.cursor.execute("""
    #         CREATE TABLE IF NOT EXISTS DB_BITGET_COORDINSTOR_LISTING_DATA (
    #             id INT AUTO_INCREMENT PRIMARY KEY,
    #             listing_time_ms INT,
    #             set_item TEXT
    #         )
    #     """)
    #     self.connection.commit()
    #     print(f"table DB_BITGET_COORDINSTOR_LISTING_DATA was created")

    def db_writer(self, set_item):  
        try:    
            listing_time_ms = set_item.get('listing_time_ms')
            set_item = str(set_item)
            self.cursor.execute("SELECT * FROM DB_BITGET_COORDINSTOR_LISTING_DATA")
            records = self.cursor.fetchall()

            if not records:
                self.cursor.execute("INSERT INTO DB_BITGET_COORDINSTOR_LISTING_DATA (listing_time_ms, set_item) VALUES (%s, %s)", (listing_time_ms, set_item))
            else:
                self.cursor.execute("UPDATE DB_BITGET_COORDINSTOR_LISTING_DATA SET listing_time_ms = %s, set_item = %s WHERE id = 1", (listing_time_ms, set_item))
            self.connection.commit()
        except Exception as ex:
            print(ex)
            return False
        finally:    
            self.connection.close()
            return True

            

