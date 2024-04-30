import time
from datetime import datetime as dttm
import datetime
import math
import re
import random
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
    
    def milliseconds_to_datetime_for_parser(self, milliseconds):        
        seconds, milliseconds = divmod(milliseconds, 1000)
        time = datetime.datetime.utcfromtimestamp(seconds)        
        return time.strftime('%Y-%m-%d %H:%M:%S')
      
    def next_one_minutes_ms(self):
        # for one and half min round min:
        return ((int(time.time() * 1000) + 90000) // 60000) * 60000

    def left_time_in_minutes_func(self, set_time):
        current_time_ms = int(time.time() * 1000)
        time_left_minutes = round((set_time - current_time_ms) / (1000 * 60), 2)
        return time_left_minutes
            
    def show_trade_time_for_calibrator(self, response_data_list):
        result_time_ms = []
        result_time_data_time = ''
        for data in response_data_list:
            try:                       
                if data['msg'] == 'success' and isinstance(data['data'], dict):
                    result_time_ms.append(data['requestTime'])
                    result_time_data_time += self.milliseconds_to_datetime(data['requestTime']) + '\n'                         
            except:
                pass
        return result_time_data_time, result_time_ms[0]
            
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

    def get_start_of_day(self):
        now = datetime.datetime.now()
        start_of_day = datetime.datetime(now.year, now.month, now.day) - datetime.timedelta(days=4)
        return int(start_of_day.timestamp() * 1000)
        # ////////////////////////////////////////////////////////////////////////////////
    def date_of_the_month(self):        
        current_time = time.time()        
        datetime_object = dttm.fromtimestamp(current_time)       
        formatted_time = datetime_object.strftime('%d')
        return int(formatted_time) 
    
    @log_exceptions_decorator
    def from_string_to_date_time(self, date_time_str):
        pattern = r'(\d{1,2})(?:st|nd|rd|th)? (\w+) (\d{4})(?:, (\d{1,2}):(\d{2}))? \(UTC\)'

        match = re.match(pattern, date_time_str)
        if match: 
            day = int(match.group(1))
            month_str = match.group(2)
            year = int(match.group(3))
            hour = int(match.group(4))
            minute = int(match.group(5))
            months = {
                'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
            }
            month = months.get(month_str)
            if month:
                dt = dttm(year, month, day, hour, minute)
                milliseconds = int(dt.timestamp() * 1000)
                return milliseconds
        return

    def symbol_extracter(self, text):
        try:  
            unik_symbol_dict = {
                "（": ' (',
                "（ ": ' (',  
                '）': ') ',
                ' ）': ') ',  
                "( ": '(',
                " )": ')',
            } 

            for k, v in unik_symbol_dict.items():
                text = text.replace(k, v)  
            matches = re.findall(r'\((.*?)\)', text)
            return [re.sub(r'[\(\)\.,\-!]', '', match) for match in matches] 
        except:
            pass
        return []
       
    # ////////////////////////////////////////////////////////////////////////////////
    @log_exceptions_decorator
    def set_list_formator(self, find_data):
        unique_data = {}
        for item in find_data:
            time_ms = item["listing_time_ms"]
            if time_ms not in unique_data:
                unique_data[time_ms] = {
                    "symbol_list": item["symbol_list"],
                    "t100_mode_pause_server1": 1.6,
                    "t100_mode_pause_server2": random.randrange(12,22)/ 10,
                    "t100_mode_pause_server3": random.randrange(12,22)/ 10,
                    "t100_mode_pause_server4": random.randrange(12,22)/ 10,
                    "listing_time_ms": time_ms,
                    "listing_time": item["listing_time"]
                }
            else:                
                new_item = {
                    "symbol_list": unique_data[time_ms]["symbol_list"] + item["symbol_list"],
                    "t100_mode_pause_server1": unique_data[time_ms]["t100_mode_pause_server1"],
                    "t100_mode_pause_server2": unique_data[time_ms]["t100_mode_pause_server2"],
                    "t100_mode_pause_server3": unique_data[time_ms]["t100_mode_pause_server3"],
                    "t100_mode_pause_server4": unique_data[time_ms]["t100_mode_pause_server4"],
                    "listing_time_ms": time_ms,
                    "listing_time": item["listing_time"]
                }
                unique_data[time_ms] = new_item

        return list(unique_data.values())      

    @log_exceptions_decorator
    def start_data_to_item(self, start_data):
        set_list = sorted(self.set_list_formator(start_data), key=lambda x: x["listing_time_ms"], reverse=False)
        try:
            return set_list[0]
        except Exception as ex:
            print(ex)
        return {}
    

# set_item.update(default_params)