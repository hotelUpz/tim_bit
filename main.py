import os
import inspect
import time
import random
from connectorss import CONNECTOR_TG
from utils import UTILS
from info_pars import ANNONCEMENT 
from db_coordinator import DB_COOORDINATOR
from log import total_log_instance, log_exceptions_decorator
current_file = os.path.basename(__file__)

class TEMPLATES(CONNECTOR_TG, UTILS):
    def __init__(self) -> None:
        super().__init__()

    def send_mess_to_tg(self, text):
        self.last_message.text = self.connector_func(self.last_message, text)

    def handle_exception(self, ex, line):
        error_message = f"An error occurred in file '{current_file}', line {line}: {ex}"
        print(error_message)
        self.send_mess_to_tg(error_message)
    
    @log_exceptions_decorator
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

    @log_exceptions_decorator   
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

    @log_exceptions_decorator
    def db_fetch_template(self, dbb_coordinator_instasnce, set_item):
        db_connect_true = dbb_coordinator_instasnce.db_connector()
        if db_connect_true:
            dbb_coordinator_repl = dbb_coordinator_instasnce.db_writer(set_item) 
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
                    self.send_mess_to_tg(f"retry_counter_: {i+1}")

                    if not self.trading_little_temp(test_set_item):
                        self.send_mess_to_tg(f'Some problems with placing buy market orders on calibration step...\n\nself.common_delay_time_ms: {self.common_delay_time_ms}')
                        self.test_listing_time_ms += 30000
                        time.sleep(0.1)
                        continue

                    result_time_data_time, result_time_ms = self.show_trade_time_for_calibrator(self.response_data_list)
                    self.send_mess_to_tg(result_time_data_time)

                    if -5 <= result_time_ms - self.test_listing_time_ms <= 20:
                        good_test_flag = True
                        self.send_mess_to_tg(f"good_test_flag: {str(good_test_flag)}")
                        good_test_counter += 1
                    elif result_time_ms - self.test_listing_time_ms < -5:
                        self.send_mess_to_tg("self.test_listing_time_ms - result_time_ms < -5")
                        self.common_delay_time_ms -= 5
                    elif result_time_ms - self.test_listing_time_ms > 20:
                        self.send_mess_to_tg("self.test_listing_time_ms - result_time_ms > 20")
                        self.common_delay_time_ms += 5

                    self.send_mess_to_tg(f"self.common_delay_time_ms: {self.common_delay_time_ms}")
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
            self.send_mess_to_tg("Some problems with calibration...")
            print("Some problems with calibration...")

        self.trades_garbage()

    @log_exceptions_decorator
    def buy_manager(self, set_item):      
        self.last_message.text = self.connector_func(self.last_message, "It is waiting time for buy!...")
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
    @log_exceptions_decorator 
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
        # self.send_mess_to_tg(f"Server #Railway#{self.railway_server_number} <<{self.market_place}>>")
        show_counter = 0
        pass_set_to_previous_flag = True
        first_iter = True
        previous_set_item = {}
        last_listing_time_ms = None

        if self.controls_mode == 'a':  
            bg_parser = ANNONCEMENT(self.proxy_host, self.proxy_port, self.proxy_username, self.proxy_password)
            db_coordinator = DB_COOORDINATOR(self.db_host, self.db_port, self.db_user, self.db_password, self.db_name)
            
            while True:                
                start_data = []
                temporary_set_item = {}                
                if self.stop_flag:
                    # self.send_mess_to_tg(f"Server #Railway#{self.railway_server_number} was stopped!")
                    self.run_flag = False
                    return

                time_diff_seconds = self.work_sleep_manager(self.work_to, self.sleep_to)
                if time_diff_seconds:
                    # self.send_mess_to_tg("It is time to rest! Let's go to bed!")
                    time.sleep(time_diff_seconds)
                elif first_iter:
                    first_iter = False
                    # self.send_mess_to_tg("It is time to work now!")

                start_data = bg_parser.bitget_parser()
                if start_data:            
                    temporary_set_item = self.start_data_to_item(start_data)   
                    if pass_set_to_previous_flag:
                        previous_set_item = temporary_set_item
                        pass_set_to_previous_flag = False

                    try:
                        # int('sdkjhvhkj')
                        if temporary_set_item.get('listing_time_ms', None) > previous_set_item.get('listing_time_ms', None):
                            temporary_set_item = previous_set_item
                    except Exception as ex:
                        self.handle_exception(ex, inspect.currentframe().f_lineno)

                    last_listing_time_ms = temporary_set_item.get('listing_time_ms', None)
                    show_counter += 1
                    # self.send_mess_to_tg(str(temporary_set_item))
                    print(temporary_set_item)
                    if show_counter == 3:
                        try:
                            temporary_set_item.update(self.set_item)
                            self.db_fetch_template(db_coordinator, temporary_set_item)
                            # self.send_mess_to_tg(str(temporary_set_item))
                            show_counter = 0
                        except Exception as ex:
                            self.handle_exception(ex, inspect.currentframe().f_lineno)
                else:
                    print(f"Server #Railway#{self.railway_server_number} There is no actual trading data yet!..")
                    # self.send_mess_to_tg(f"Server #Railway#{self.railway_server_number} There is no actual trading data yet!..")

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
                            total_log_instance.json_to_buffer('PARS', cur_time, start_data)
                            cur_time = int(time.time() * 1000)
                            total_log_instance.json_to_buffer('START', cur_time, [temporary_set_item])
                            json_file = total_log_instance.get_json_data()                
                            self.bot.send_document(self.last_message.chat.id, json_file)   
                            log_file = total_log_instance.get_logs()
                            self.bot.send_document(self.last_message.chat.id, log_file)                            
                            time.sleep((last_listing_time_ms - int(time.time() * 1000)) / 1000)
                        except Exception as ex:
                            self.handle_exception(ex, inspect.currentframe().f_lineno)

                        previous_set_item = {}
                        last_listing_time_ms = None                        
                        pass_set_to_previous_flag = True
                        continue
                    
                # self.send_mess_to_tg(f"Server #Railway#{self.railway_server_number} pause...")
                print('pause')
                # time.sleep(random.uniform(239, 299))
                time.sleep(random.uniform(20, 30))

        self.send_mess_to_tg(self.SOLI_DEO_GLORIA)

class TG_MANAGER(MAIN_CONTROLLER):
    def __init__(self):
        super().__init__()
        
    def run(self): 
        try: 
            @self.bot.message_handler(commands=['start'])
            @self.bot.message_handler(func=lambda message: message.text == 'START')
            def handle_start_input(message):
                if self.block_acess_flag:
                    response_message = "Don't bullshit!"
                    message.text = self.connector_func(message, response_message)
                else:   
                    self.start_day_date = self.date_of_the_month()          
                    self.bot.send_message(message.chat.id, "Please enter a secret token...", reply_markup=self.menu_markup)                   
                    self.start_flag = True

            @self.bot.message_handler(func=lambda message: self.start_flag)
            def handle_start_redirect(message):                
                try:
                    cur_day_date = None                    
                    value_token = message.text.strip()
                    cur_day_date = self.date_of_the_month()

                    if self.start_day_date != cur_day_date:
                        self.start_day_date = cur_day_date
                        self.block_acess_flag = False 
                        self.block_acess_counter = 0

                    if value_token == self.seq_control_token and not self.block_acess_flag:
                        self.seq_control_flag = True 
                        self.start_flag = False
                        self.stop_flag = False
                        # ////////////////////////////////////////////////////////////////////
                        try:                                                       
                            response_message = 'God bless you Nik!'
                            # print(response_message) 
                            self.bot.send_message(message.chat.id, response_message, reply_markup=self.menu_markup)
                            self.last_message = message
                            if self.run_flag:
                                message.text = self.connector_func(message, "Bot is run at current moment. Please stop bot firstable than try again...")
                            else:
                                self.default_trade_vars()                                
                                self.main_func()  
                        except Exception as ex:
                            self.handle_exception(ex, inspect.currentframe().f_lineno)
                        # ////////////////////////////////////////////////////////////////////                       

                    elif value_token != self.seq_control_token and not self.block_acess_flag:                               
                        self.block_acess_counter += 1
                        if self.block_acess_counter >= 3:
                            self.block_acess_flag = True
                            self.start_flag = False 
                            response_message = "The number of attempts has been exhausted. Please try again later..."
                            message.text = self.connector_func(message, response_message)
                        else:
                            response_message = "Please put a valid token!"
                            message.text = self.connector_func(message, response_message)
                except Exception as ex:
                    self.handle_exception(ex, inspect.currentframe().f_lineno)        

            @self.bot.message_handler(func=lambda message: message.text == 'STOP')             
            def handle_stop(message):
                if self.seq_control_flag and not self.block_acess_flag:
                    self.bot.send_message(message.chat.id, "Are you sure you want to stop the program? (y/n)")
                    self.stop_redirect_flag = True
                else:
                    self.bot.send_message(message.chat.id, "Please enter START for verification")

            @self.bot.message_handler(func=lambda message: self.stop_redirect_flag)             
            def handle_stop_redirect(message):
                self.stop_redirect_flag = False
                if message.text.strip().upper() == 'Y':                    
                    self.stop_flag = True 
                    self.bot.send_message(message.chat.id, "Please waiting...")                   
                else:
                    self.bot.send_message(message.chat.id, "Program was not stopped.")  
            # /////////////////////////////////////////////////////////////////////////////////////////////////////
            @self.bot.message_handler(func=lambda message: message.text == 'SETTINGS')             
            def handle_settings(message):
                if self.seq_control_flag and not self.block_acess_flag:
                    try:
                        message.text = self.connector_func(message, "Please enter a delay_ms, depo size and server_number using shift (e.g: 111 21 1)")
                        self.settings_redirect_flag = True
                    except Exception as ex:
                        self.handle_exception(ex, inspect.currentframe().f_lineno)
                else:
                    self.bot.send_message(message.chat.id, "Please enter START for verification")               

            @self.bot.message_handler(func=lambda message: self.settings_redirect_flag)             
            def handle_settings_redirect(message):
                try:
                    self.settings_redirect_flag = False
                    delay_time_ms = None
                    depo = None
                    dataa = [x for x in message.text.strip().split(' ') if x.strip()]  
                    delay_time_ms = int(float(dataa[0]))   
                    depo = int(float(dataa[1]))
                    server_index = int(float(dataa[2]))
                    if len(dataa) == 3:
                        for i in range(1, 5, 1):  
                            if i == server_index: 
                                self.set_item[f'depo_server{i}'] = depo
                                self.set_item[f'delay_time_ms_server{i}'] = delay_time_ms
                        mess_temp = '\n'.join(list(f"{k}: {v}" for k, v in self.set_item.items()))
                        message.text = self.connector_func(message, mess_temp)
                    else:
                        message.text = self.connector_func(message, f"Please enter a valid options...")
                except Exception as ex:
                    self.handle_exception(ex, inspect.currentframe().f_lineno)
            # /////////////////////////////////////////////////////////////////////////////////////////////////////

            # self.bot.polling()
            self.bot.infinity_polling()
        except Exception as ex:
            print(ex)

if __name__=="__main__": 
    MAIN_CONTROLLER().main_func() 
    # print('Please go to the Telegram bot interface!')     
    # bot = TG_MANAGER()   
    # bot.run()