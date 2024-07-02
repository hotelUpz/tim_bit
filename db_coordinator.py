import mysql.connector
import time
import random 
import ast
from utils import UTILS

class DB_COOORDINATOR(UTILS):
    def __init__(self) -> None:
        super().__init__()
        self.db_connector = self.log_exceptions_decorator(self.db_connector)
    
    def db_connector(self):
        config = {
            'user': self.db_user,
            'password': self.db_password,            
            'host': self.db_host,
            'port': self.db_port,
            'database': self.db_name,
        }
        for _ in range(2):
            try:
                self.connection = mysql.connector.connect(**config)      
                # print("Writerr connection established")
                self.cursor = self.connection.cursor()
                return True
            except Exception as ex:
                self.handle_exception(ex)
                time.sleep(random.randrange(1,4))                
        return False
        
    def read_db_data(self):
        records = []
        try:
            self.cursor.execute("SELECT * FROM DB_BITGET_COORDINSTOR_LISTING_DATA")
            records = self.cursor.fetchall()
        except Exception as ex:
            self.handle_exception(ex)
            return
        finally:
            self.connection.close()
            return records

    def formate_db_data(self, db_reading_data):
        try: 
            set_item = {}  
            set_item = ast.literal_eval(db_reading_data[0][1])        
            return set_item.get("listing_time_ms", None), set_item
        except Exception as ex:
            self.handle_exception(ex)
        return {}, None

            

