import time
import random
from db_coordinator import DB_COOORDINATOR
import os
import inspect
current_file = os.path.basename(__file__) #

class TEMPLATES(DB_COOORDINATOR):
    def __init__(self) -> None:
        super().__init__()
        self.buy_market_temp = self.log_exceptions_decorator(self.buy_market_temp) 
        self.sell_market_temp = self.log_exceptions_decorator(self.sell_market_temp) 
        self.db_fetch_template = self.log_exceptions_decorator(self.db_fetch_template)
    
    def buy_market_temp(self, symbol):  
        response = self.place_market_order(symbol, 'BUY', self.depo_test)                
        response = response.json() 
        response['symbol'] = symbol
        response['side'] = 'BUY'
        response['status'] = 'filled'                           
        self.response_data_list.append(response)                   
        if response['msg'] == 'success': 
            # print('buy success!')
            self.last_message.text = self.connector_func(self.last_message, 'buy success!')
            self.response_success_list.append(response)
       
    def sell_market_temp(self, item):      
        response = None               
        response = self.place_market_order(item['data'][0]['symbol'], 'SELL', item['qnt_to_sell_start'])           
        response = response.json()
        response['symbol'] = item['data'][0]['symbol']
        response['side'] = 'SELL' 
        response['status'] = 'filled' 
        self.response_data_list.append(response)   
        if response['msg'] == 'success':   
            # print('sell success!')   
            self.last_message.text = self.connector_func(self.last_message, 'sell success!') 
        else:                
            # print(f"Symbol: {item['data'][0]['symbol']}:... some problems with placing the sell order") 
            self.last_message.text = self.connector_func(self.last_message, f"Symbol: {item['data'][0]['symbol']}:... some problems with placing the sell order")
    
    def db_fetch_template(self, set_item):
        db_connect_true = self.db_connector()
        if db_connect_true:
            dbb_coordinator_repl = self.db_writer(set_item) 
            if dbb_coordinator_repl:
                self.last_message.text = self.connector_func(self.last_message, 'Writing set_item data was making successfully!')
            else:
                self.last_message.text = self.connector_func(self.last_message, 'Some problems with writing set_item data...')
        else:
            self.last_message.text = self.connector_func(self.last_message, 'Some problem with db connecting...')                               

class MANAGER(TEMPLATES):
    def __init__(self) -> None:
        super().__init__()

    def delay_manager(self):
        def delay_calibrator(test_set_item):
            good_test_flag = False
            good_test_counter = 0
            retry_limit_counter = 5

            for i in range(retry_limit_counter):
                try:
                    if good_test_counter == 2:
                        return True
                    elif not good_test_flag:
                        good_test_counter = 0

                    good_test_flag = False
                    self.handle_messagee(f"retry_counter_: {i+1}")

                    if not self.trading_little_temp(test_set_item):
                        self.handle_messagee(f'Some problems with placing buy market orders on calibration step...\n\nself.common_delay_time_ms: {self.common_delay_time_ms}')
                        self.test_listing_time_ms += 30000
                        time.sleep(0.1)
                        continue

                    result_time_data_time, result_time_ms = self.show_trade_time_for_calibrator(self.response_data_list)
                    self.handle_messagee(result_time_data_time)

                    if -5 <= result_time_ms - self.test_listing_time_ms <= 20:
                        good_test_flag = True
                        self.handle_messagee(f"good_test_flag: {str(good_test_flag)}")
                        good_test_counter += 1
                    elif result_time_ms - self.test_listing_time_ms < -5:
                        self.handle_messagee("self.test_listing_time_ms - result_time_ms < -5")
                        self.common_delay_time_ms -= 5
                    elif result_time_ms - self.test_listing_time_ms > 20:
                        self.handle_messagee("self.test_listing_time_ms - result_time_ms > 20")
                        self.common_delay_time_ms += 5

                    self.handle_messagee(f"self.common_delay_time_ms: {self.common_delay_time_ms}")
                    self.test_listing_time_ms += 30000
                    time.sleep(0.1)
                except Exception as ex:
                    self.handle_exception(ex, inspect.currentframe().f_lineno)
                    return False
            return True

        test_set_item = {
            "symbol_list": [self.default_test_symbol],
            "listing_time_ms": self.next_one_minutes_ms()
        }

        try:
            self.test_listing_time_ms = test_set_item['listing_time_ms']
            delay_manager_return = delay_calibrator(test_set_item)
        except Exception as ex:
            self.handle_exception(ex, inspect.currentframe().f_lineno)
            delay_manager_return = False

        if not delay_manager_return:
            self.handle_messagee("Some problems with calibration...")

        self.trades_garbage()

    def buy_manager(self, set_item):      
        self.handle_messagee("It is waiting time for buy!...")
        self.response_data_list, self.response_success_list = [], [] 
        schedule_time_ms = self.test_listing_time_ms - 4000
        time.sleep((schedule_time_ms - int(time.time()*1000))/ 1000)            
        buy_time_ms = self.test_listing_time_ms - self.common_delay_time_ms  
        try:              
            symbol = set_item["symbol_list"][0]  
        except Exception as ex:
            self.handle_exception(ex, inspect.currentframe().f_lineno)             
        self.send_fake_request(self.symbol_fake) 
        time.sleep((buy_time_ms - int(time.time()*1000))/ 1000)                
        self.buy_market_temp(symbol)            

    def trading_little_temp(self, set_item):                                
        self.buy_manager(set_item)
        if len(self.response_success_list) == 0:
            self.last_message.text = self.connector_func(self.last_message, 'Some problems with placing buy market orders...')
            return False
            # print('Some problems with placing buy market orders...')             
        return True
        # ////////////////////////////////////////////////////////
     
    def trades_garbage(self):
        symbol = self.default_test_symbol.replace('USDT', '').strip()
        qty_garbare = self.get_balance(symbol).json().get('data')[0].get('balance')
        item = {
            'data': [{'symbol': self.default_test_symbol}],
            'qnt_to_sell_start': round(float(qty_garbare)* 0.99, 2)
            
        }     
        self.sell_market_temp(item)

class MAIN_CONTROLLER(MANAGER):
    def __init__(self) -> None:
        super().__init__()

    def main_func(self): 
        self.run_flag = True
        self.send_mess_to_tg(f"Server #Railway#{self.railway_server_number} <<{self.market_place}>>")
        show_counter = 0
        pass_set_to_previous_flag = True
        first_iter = True
        previous_set_item = {}
        last_listing_time_ms = None
        
        while True:                
            start_data = []
            temporary_set_item = {}                
            if self.stop_flag:
                self.send_mess_to_tg(f"Server #Railway#{self.railway_server_number} was stopped!")
                self.run_flag = False
                return

            time_diff_seconds = self.work_sleep_manager(self.work_to, self.sleep_to)
            if time_diff_seconds:
                self.send_mess_to_tg("It is time to rest! Let's go to bed!")
                time.sleep(time_diff_seconds)
            elif first_iter:
                first_iter = False
                self.send_mess_to_tg("It is time to work now!")

            start_data = bg_parser.bitget_parser()
            if start_data:            
                temporary_set_item = self.start_data_to_item(start_data)  
                # print(temporary_set_item)
                if pass_set_to_previous_flag:
                    previous_set_item = temporary_set_item
                    pass_set_to_previous_flag = False

                try:                       
                    if temporary_set_item.get('listing_time_ms', None) > previous_set_item.get('listing_time_ms', None):
                        temporary_set_item = previous_set_item
                except Exception as ex:
                    self.handle_exception(ex, inspect.currentframe().f_lineno)

                last_listing_time_ms = temporary_set_item.get('listing_time_ms', None)
                show_counter += 1
                # self.send_mess_to_tg(str(temporary_set_item))
                # print(temporary_set_item)
                # if show_counter == 3:
                try:
                    temporary_set_item.update(self.set_item)
                    self.db_fetch_template(temporary_set_item)
                    self.handle_messagee(str(temporary_set_item))
                    show_counter = 0
                except Exception as ex:
                    self.handle_exception(ex, inspect.currentframe().f_lineno)
            else:
                print(f"Server #Railway#{self.railway_server_number} There is no actual trading data yet!..")
                self.send_mess_to_tg(f"Server #Railway#{self.railway_server_number} There is no actual trading data yet!..")

            if last_listing_time_ms:                    
                if 0 < self.left_time_in_minutes_func(last_listing_time_ms) <= 15:
                    try:
                        if self.calibrator_flag:
                            self.delay_manager()

                        for i in range(1, self.total_server_number + 1):
                            self.set_item[f'delay_time_ms_server{i}'] = self.common_delay_time_ms

                        if not temporary_set_item:
                            temporary_set_item = previous_set_item

                        temporary_set_item.update(self.set_item)
                        self.send_mess_to_tg(str(temporary_set_item))
                        self.db_fetch_template(db_coordinator, temporary_set_item)

                        cur_time = int(time.time() * 1000)
                           
                        time.sleep((last_listing_time_ms - int(time.time() * 1000)) / 1000)
                    except Exception as ex:
                        self.handle_exception(ex, inspect.currentframe().f_lineno)

                    previous_set_item = {}
                    last_listing_time_ms = None                        
                    pass_set_to_previous_flag = True
                    continue
                
            self.send_mess_to_tg(f"Server #Railway#{self.railway_server_number} pause...")
            print('pause')
            time.sleep(random.uniform(239, 299))
            # time.sleep(random.uniform(20, 30))

