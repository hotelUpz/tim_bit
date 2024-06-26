import os
from dotenv import load_dotenv
load_dotenv()

class PARAMS():
    def __init__(self) -> None:
        self.default_trade_vars()
        self.default_tg_vars()
        self.init_keys()

    def default_trade_vars(self):
        self.SOLI_DEO_GLORIA = 'Soli Deo Gloria!'      
        self.controls_mode = 'a'
        self.run_flag = False
        self.testnet_flag = False
        self.calibrator_flag = True
        self.stop_flag = False
        self.work_to = 17 # hoor in UTC
        self.sleep_to = 5 # hoor in UTC
        self.manual_data_time = "2024-04-17 23:14:00" # utc time
        self.manual_symbol_list = ['ARBUSDT', 'BGBUSDT', 'TONCOINUSDT']
        self.default_test_symbol = 'ARBUSDT'
        self.response_data_list, self.response_success_list = [], []
        self.threads_flag = False
        self.max_symbol_list_slice = 2       
        self.symbol_list_el_position = 0 #fj,bh
        self.market_place = 'bitget'
        self.symbol_fake = 'T'
        self.depo = 20
        self.sell_mode = 't100' # t100 -- sell for all qty by time
        self.delay_flag = True # True  
        self.delay_default_time_ms = 95   
        self.delay_time_ms = 95
        self.listing_time_ms = None
        self.incriment_time_ms = 0
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
        # print(self.tg_api_token)
        self.seq_control_token = os.getenv("ACESS_TOKEN", "")