import os
from dotenv import load_dotenv
load_dotenv()

class PARAMS():
    def __init__(self) -> None:
        self.SOLI_DEO_GLORIA = 'Soli Deo Gloria!'  
        self.railway_server_number = 1            
        self.stop_flag = False
        self.work_to = 17 # hoor in UTC
        self.sleep_to = 5 # hoor in UTC
        self.response_data_list, self.response_success_list = [], []  
        self.symbol_list_el_position = 1
        self.trade_duble_flag = True
        self.market_place = 'bitget'
        self.symbol_fake = 'T'
        self.depo = 10
        self.sell_mode = 't100' # t100 -- sell for all qty by time
        self.delay_time_ms = 90
        self.listing_time_ms = None
        self.incriment_time_ms = self.railway_server_number - 1    
        self.sell_attempts_number = 2
        self.timedelta_stamps = 'hours'
        self.timedelta_stamps_value = 1
        self.default_params = {
            "market_place": self.market_place,
            "sell_mode": self.sell_mode,      
            "incriment_time_ms": self.incriment_time_ms,          
            "sell_attempts_number": self.sell_attempts_number,
        }
        self.init_keys()

    def init_keys(self):  
        self.api_key  = os.getenv(f"{self.market_place.upper()}_API_PUBLIC_KEY", "")
        self.api_secret = os.getenv(f"{self.market_place.upper()}_API_PRIVATE_KEY", "") 
        self.api_passphrase = os.getenv("API_PASSPHRASE", "")
        self.tg_api_token = os.getenv("TG_TOKEN", "")