import time
from datetime import datetime as dttm
import datetime
import math
from log import log_exceptions_decorator

def server_to_utc_difference_counter():
    server_time_naive = dttm.now()
    print(f"server_time_naive: {server_time_naive}")
    utc_time = dttm.utcnow()
    print(f"utc_time: {utc_time}")
    time_difference = server_time_naive - utc_time
    total_seconds = abs(time_difference.total_seconds()) * 1000
    total_seconds = math.ceil(total_seconds)
    if total_seconds < 10:
        return 0
    return total_seconds

time_correction = server_to_utc_difference_counter()
print("ms difference:", time_correction)

class UTILS():
    def __init__(self) -> None:
        pass

    def datetime_to_milliseconds(self, datetime_str):           
        dt_obj = time.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        return int(time.mktime(dt_obj) * 1000)

    def milliseconds_to_datetime(self, milliseconds):
        milliseconds = milliseconds + time_correction
        seconds, milliseconds = divmod(milliseconds, 1000)
        time = datetime.datetime.utcfromtimestamp(seconds)
        milliseconds_str = str(milliseconds).zfill(3)
        return time.strftime('%Y-%m-%d %H:%M:%S') + '.' + milliseconds_str

    def left_time_in_minutes_func(self, set_time):
        current_time_ms = int(time.time() * 1000)
        time_left_minutes = round((set_time - current_time_ms) / (1000 * 60), 2)
        return time_left_minutes
            
    def show_trade_time(self, response_data_list, market_place):
        result_time = ''
        dataa = None
        for i, data in enumerate(response_data_list):
            try:                                
                if market_place == 'bitget':  
                    dataa = data['requestTime'] 
                elif market_place == 'bybit':  
                    dataa = data['time']                              
                formatted_time = self.milliseconds_to_datetime(dataa)               
                form_time = f"{data['side']}: {formatted_time}"
                if data['msg'] == 'success' and isinstance(data['data'], dict):
                    result_time += data['symbol'] + ' ' + form_time + '\n' 
                response_data_list[i]["process_time"] = form_time            
            except:
                pass
        return result_time, response_data_list
      
    def work_sleep_manager(self, work_to, sleep_to):
        if not work_to or not sleep_to:
            return None
        current_time_utc = time.gmtime(time.time())
        current_hour = current_time_utc.tm_hour
        if not (sleep_to <= current_hour < work_to):
            current_time_utc = time.gmtime(time.time())
            desired_time_utc = time.struct_time((current_time_utc.tm_year, current_time_utc.tm_mon, current_time_utc.tm_mday + 1, sleep_to, 0, 0, 0, 0, 0))
            time_diff_seconds = time.mktime(desired_time_utc) - time.mktime(current_time_utc)
            print("It is time to rest! Let's go to bed!")
            return time_diff_seconds
        return None


