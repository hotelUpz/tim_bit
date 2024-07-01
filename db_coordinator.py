import mysql.connector
import time
import random 
import ast
from info_pars import ANNONCEMENT
import os
import inspect
current_file = os.path.basename(__file__)

class DB_COOORDINATOR(ANNONCEMENT):
    def __init__(self) -> None:
        super().__init__()
        self.db_connector = self.log_exceptions_decorator(self.db_connector)
        self.create_table = self.log_exceptions_decorator(self.create_table)

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
                self.handle_exception(ex, inspect.currentframe().f_lineno)
                time.sleep(random.randrange(1,4))                
        return False

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS DB_BITGET_COORDINSTOR_LISTING_DATA (
                id INT AUTO_INCREMENT PRIMARY KEY,                
                set_item TEXT
            )
        """)
        self.connection.commit()
        self.handle_messagee(f"table DB_BITGET_COORDINSTOR_LISTING_DATA was created")

    def db_writer(self, set_item):  
        try:           
            set_item = str(set_item)
            self.cursor.execute("SELECT * FROM DB_BITGET_COORDINSTOR_LISTING_DATA")
            records = self.cursor.fetchall()

            if not records:
                self.cursor.execute("INSERT INTO DB_BITGET_COORDINSTOR_LISTING_DATA (set_item) VALUES (%s)", (set_item,))
            else:
                self.cursor.execute("UPDATE DB_BITGET_COORDINSTOR_LISTING_DATA SET set_item = %s WHERE id = 1", (set_item,))
            self.connection.commit()
            return True
        except Exception as ex:
            self.handle_exception(ex, inspect.currentframe().f_lineno)
            return False
        finally:    
            self.connection.close()

            

