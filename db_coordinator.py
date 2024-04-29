from utils import UTILS, log_exceptions_decorator, time_correction

class DB_COOORDINATOR(UTILS):
    def __init__(self) -> None:
        super().__init__() 

    def fetch_settings_data(self):
        set_item, self_listing_time_ms = 1,1
        return set_item, self_listing_time_ms