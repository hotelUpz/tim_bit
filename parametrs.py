import os
from dotenv import load_dotenv
load_dotenv()

class PARAMS():
    def __init__(self) -> None:
        self.SOLI_DEO_GLORIA = 'Soli Deo Gloria!'      
        self.controls_mode = 'a'
        self.testnet_flag = False
        self.calibrator_flag = True
        self.stop_flag = False
        self.work_to = 18 # hoor in UTC
        self.sleep_to = 5 # hoor in UTC
        self.manual_data_time = "2024-04-17 23:14:00" # utc time
        self.manual_symbol_list = ['ARBUSDT', 'BGBUSDT', 'TONCOINUSDT']
        self.default_test_symbol = 'ARBUSDT'
        self.response_data_list, self.response_success_list = [], []
        self.threads_flag = False
        self.max_symbol_list_slice = 2       
        self.symbol_list_el_position = 0
        self.market_place = 'bitget'
        self.symbol_fake = 'T'
        self.depo = 11
        self.sell_mode = 't100' # t100 -- sell for all qty by time
        self.delay_flag = True # True  
        self.delay_default_time_ms = 97   
        self.delay_time_ms = 97
        self.listing_time_ms = None
        self.incriment_time_ms = 1
        self.pre_start_pause = 0 
        self.t100_mode_pause = None        
        self.sell_attempts_number = 2
        self.timedelta_stamps = 'hours'
        self.timedelta_stamps_value = 1
        self.default_params = {
            "controls_mode": self.controls_mode,
            "testnet_flag": self.testnet_flag,
            "calibrator_flag": self.calibrator_flag,
            "market_place": self.market_place,
            "sell_mode": self.sell_mode,
            "delay_flag": self.delay_flag,
            "incriment_time_ms": self.incriment_time_ms,
            "pre_start_pause": self.pre_start_pause,
            "sell_attempts_number": self.sell_attempts_number,
            "max_symbol_list_slice": self.max_symbol_list_slice
        }
        self.init_keys()

    def init_keys(self):  
        self.api_key  = os.getenv(f"{self.market_place.upper()}_API_PUBLIC_KEY", "")
        self.api_secret = os.getenv(f"{self.market_place.upper()}_API_PRIVATE_KEY", "") 
        self.api_passphrase = os.getenv("API_PASSPHRASE", "")
        self.tg_api_token = os.getenv("TG_TOKEN", "")