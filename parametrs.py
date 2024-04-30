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
        self.railway_server_number = 'base'   
        self.controls_mode = 'a'
        self.run_flag = False
        self.calibrator_flag = False
        self.stop_flag = False        
        self.work_to = 23 # hoor in UTC
        self.sleep_to = 5 # hoor in UTC
        self.default_test_symbol = 'ARBUSDT'
        self.response_data_list, self.response_success_list = [], []
        self.threads_flag = False    
        self.symbol_list_el_position = 0 #fj,bh
        self.market_place = 'bitget'
        self.symbol_fake = 'T'
        self.common_depo = 20
        self.depo_test = 10
        self.sell_mode = 't100' # t100 -- sell for all qty by time
        self.common_delay_time_ms = 95
        self.listing_time_ms = None
        self.incriment_time_ms = 0
        self.sell_attempts_number = 2
        self.timedelta_stamps = 'hours'
        self.timedelta_stamps_value = 1
        self.set_item = {
            "depo_server1": self.common_depo,
            "delay_time_ms_server1": self.common_delay_time_ms,
            "depo_server2": self.common_depo,
            "delay_time_ms_server2": self.common_delay_time_ms,
            "depo_server3": self.common_depo,
            "delay_time_ms_server3": self.common_delay_time_ms,
            "depo_server4": self.common_depo,
            "delay_time_ms_server4": self.common_delay_time_ms,
            # //////////////////////////////////////////////////
            "market_place": self.market_place,
            "calibrator_flag": self.calibrator_flag,            
            "sell_mode": self.sell_mode,
            "incriment_time_ms": self.incriment_time_ms,
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
        self.seq_control_token = os.getenv("ACESS_TOKEN", "")