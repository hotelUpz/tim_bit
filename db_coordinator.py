from utils import UTILS
import mysql.connector

class DB_COOORDINATOR(UTILS):
    def __init__(self, host, port, user, password, database) -> None:
        super().__init__()
        self.connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()        

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS DB_BITGET_COORDINSTOR_LISTING_DATA (
                id INT AUTO_INCREMENT PRIMARY KEY,
                listing_time_ms INT,
                set_item TEXT
            )
        """)
        self.connection.commit()

    def db_writer(self, set_item):
        self.create_table()
        listing_time_ms = set_item.get('listing_time_ms')
        set_item = str(set_item)
        self.cursor.execute("SELECT * FROM DB_BITGET_COORDINSTOR_LISTING_DATA")
        records = self.cursor.fetchall()

        if not records:
            self.cursor.execute("INSERT INTO DB_BITGET_COORDINSTOR_LISTING_DATA (listing_time_ms, set_item) VALUES (%s, %s)", (listing_time_ms, set_item))
        else:
            db_reading_data = self.read_data()
            print(x)
            for x in db_reading_data:
                print(x)
            self.cursor.execute("UPDATE data SET listing_time_ms = %s, set_item = %s WHERE id = 1", (listing_time_ms, set_item))
        
        self.connection.commit()
        # //////////////////////////////
        self.connection.close()

    def read_data(self):
        self.cursor.execute("SELECT * FROM DB_BITGET_COORDINSTOR_LISTING_DATA")
        records = self.cursor.fetchall()
        self.connection.close()
        return records

            

