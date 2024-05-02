import os
from dotenv import load_dotenv
load_dotenv()

class PARAMS():
    def __init__(self) -> None:
        self.SOLI_DEO_GLORIA = 'Soli Deo Gloria!'
        self.default_trade_vars()
        self.default_tg_vars()
        self.init_keys()

    def default_trade_vars(self):
        self.market_place = 'bitget'  
        self.response_data_list, self.response_success_list = [], []  
        self.incriment_time_ms = self.railway_server_number = 1  
        self.symbol_list_el_position = 0
        self.listing_time_ms = None        
        self.stop_flag = False
        self.trade_duble_flag = True
        self.symbol_fake = 'T'
        self.sell_mode = 't100' # t100 -- sell for all qty by time       
        self.sell_attempts_number = 2
        self.work_to = 17 # hoor in UTC
        self.sleep_to = 5 # hoor in UTC 
        self.timedelta_stamps = 'hours'
        self.timedelta_stamps_value = 1

    def default_tg_vars(self):    
        self.block_acess_flag = False
        self.start_flag = False
        self.start_day_date = None
        self.block_acess_counter = 0
        self.seq_control_flag = False
        self.seq_control_token = False
        self.dont_seq_control = False
        self.stop_redirect_flag = False  
        self.settings_redirect_flag = False 

    def init_keys(self):  
        self.api_key  = os.getenv(f"{self.market_place.upper()}_API_PUBLIC_KEY", "")
        self.api_secret = os.getenv(f"{self.market_place.upper()}_API_PRIVATE_KEY", "")        
        self.api_passphrase = os.getenv("API_PASSPHRASE", "")
        self.tg_api_token = os.getenv("TG_TOKEN", "")
        self.seq_control_token = os.getenv("ACESS_TOKEN", "")
        # ////////////////for db//////////////////////////////:
        self.db_user = os.getenv("DB_USER", "")
        self.db_password = os.getenv("DB_PASSWORD", "")
        self.db_name = os.getenv("DB_NAME", "")
        self.db_host = os.getenv("DB_HOST", "")
        self.db_port = os.getenv("DB_PORT", "")