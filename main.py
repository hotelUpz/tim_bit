import decimal
import time
import random
import concurrent.futures
import telebot
from telebot import types
from api_bitget import BITGET_API
from utils import UTILS
from log import total_log_instance, log_exceptions_decorator

class CONNECTOR_TG(BITGET_API, UTILS):
    def __init__(self):  
        super().__init__()  
        # dfjvn
        self.bot = telebot.TeleBot(self.tg_api_token)
        self.menu_markup = self.create_menu() 
        self.last_message = None

    def create_menu(self):
        menu_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        button1 = types.KeyboardButton("START")
        button2 = types.KeyboardButton("STOP")
        button3 = types.KeyboardButton("SETTINGS")       
        menu_markup.add(button1, button2, button3)        
        return menu_markup

class TG_ASSISTENT(CONNECTOR_TG):
    def __init__(self):
        super().__init__()

    def connector_func(self, message, response_message):
        retry_number = 3
        decimal = 1.1       
        for i in range(retry_number):
            try:
                self.bot.send_message(message.chat.id, response_message)                
                return message.text
            except Exception as ex:
                print(ex)

                time.sleep(1.1 + i*decimal)                   
        return None

class TEMPLATES(TG_ASSISTENT):
    def __init__(self) -> None:
        super().__init__()
    
    @log_exceptions_decorator
    def buy_market_temp(self, symbol):  
        # int('dfjgfj,')   
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
                    if (good_test_counter == 2):                                            
                        return True
                    elif not good_test_flag:
                        good_test_counter = 0

                    good_test_flag = False
                    self.last_message.text = self.connector_func(self.last_message, f"retry_counter_: {i+1}")
                    # print(f"retry_counter_: {i}")
                                      
                    if not self.trading_little_temp(test_set_item):
                        self.last_message.text = self.connector_func(self.last_message, 'Some problems with placing buy market orders on calibration step...' + '\n\n' + f"self.common_delay_time_ms: {self.common_delay_time_ms}")
                        # print('Some problems with placing buy market orders on calibration step...')
                        # print(f"self.common_delay_time_ms: {self.common_delay_time_ms}")
                        self.listing_time_ms += 30000
                        time.sleep(0.1)
                        continue
                    result_time_data_time, result_time_ms = self.show_trade_time_for_calibrator(self.response_data_list)
                    self.last_message.text = self.connector_func(self.last_message, result_time_data_time)
                    # print(result_time_data_time)
                    if -5 <= result_time_ms - self.listing_time_ms <= 20:
                        good_test_flag = True
                        self.last_message.text = self.connector_func(self.last_message, f"good_test_flag: {str(good_test_flag)}")
                        # print(f"good_test_flag: {good_test_flag}")
                        good_test_counter += 1
                    elif result_time_ms - self.listing_time_ms < -5:
                        self.last_message.text = self.connector_func(self.last_message, "self.listing_time_ms - result_time_ms < 4")
                        # print("self.listing_time_ms - result_time_ms < 4")
                        self.common_delay_time_ms -= 5
                    elif result_time_ms - self.listing_time_ms > 20:
                        self.last_message.text = self.connector_func(self.last_message, "self.listing_time_ms - result_time_ms > 20")
                        # print("self.listing_time_ms - result_time_ms > 20")
                        self.common_delay_time_ms += 5
                    
                    self.last_message.text = self.connector_func(self.last_message, f"self.common_delay_time_ms: {self.common_delay_time_ms}")
                    # print(f"self.common_delay_time_ms: {self.common_delay_time_ms}")
                    self.listing_time_ms += 30000
                    time.sleep(0.1)
                except Exception as ex:
                    # print(f"main 117: {ex}")
                    self.last_message.text = self.connector_func(self.last_message, ex)
                    return False
            return True
        start_listing_time_ms = self.listing_time_ms
        test_set_item = {
                "symbol_list": [self.default_test_symbol],
                "listing_time_ms": self.next_one_minutes_ms()                    
            }
                
        try:
            delay_manager_return = False            
            self.listing_time_ms = test_set_item['listing_time_ms']
            delay_manager_return = delay_calibrator(test_set_item)
        except Exception as ex:
            print(ex)
        if not delay_manager_return:
            self.last_message.text = self.connector_func(self.last_message, "Some problems with calibration...")
            print("Some problems with calibration...")
        self.listing_time_ms = start_listing_time_ms
        self.trades_garbage()

    @log_exceptions_decorator
    def buy_manager(self, set_item):      
        self.last_message.text = self.connector_func(self.last_message, "It is waiting time for buy!...")
        self.response_data_list, self.response_success_list = [], [] 
        schedule_time_ms = self.listing_time_ms - 4000
        time.sleep((schedule_time_ms - int(time.time()*1000))/ 1000)            
        buy_time_ms = self.listing_time_ms - self.common_delay_time_ms  
        try:              
            symbol = set_item["symbol_list"][0]  
        except Exception as ex:
            print(ex)             
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
        print(f'<<{self.market_place}>>')
        # self.last_message.text = self.connector_func(self.last_message, f"Server #Railway#{self.railway_server_number} <<{self.market_place}>>")
        start_data = []
        set_item = {}
        show_counter = 0
        first_req_flag = True
        previous_set_item = {}
        if self.controls_mode == 'a':  
            from info_pars import ANNONCEMENT 
            from db_coordinator import DB_COOORDINATOR
            bg_parser = ANNONCEMENT()
            # print(self.db_host, self.db_port, self.db_user, self.db_password, self.db_name)
            dbb_coordinator = DB_COOORDINATOR(self.db_host, self.db_port, self.db_user, self.db_password, self.db_name) 

            # data = {'symbol_list': ['STYLEUSDT'], 't100_mode_pause_server1': 1.6, 't100_mode_pause_server2': 1.2, 't100_mode_pause_server3': 2.1, 't100_mode_pause_server4': 1.6, 'listing_time_ms': 1714561200000, 'listing_time': '2024-05-01 14:00:00', 'depo_server1': 400, 'delay_time_ms_server1': 400, 'depo_server2': 300, 'delay_time_ms_server2': 300, 'depo_server3': 20, 'delay_time_ms_server3': 95, 'depo_server4': 100, 'delay_time_ms_server4': 100, 'market_place': 'bitget', 'calibrator_flag': False, 'sell_mode': 't100', 'incriment_time_ms': 0}
            # dbb_coordinator.db_connector()
            # dbb_coordinator.create_table()
            # dbb_coordinator.db_writer(data)
            # return
            while True:
                previous_set_item = set_item
                start_data = []
                set_item = {} 
                self.listing_time_ms = None
                # ///////////////// stop logic ///////////////////////////  
                if self.stop_flag:
                    self.last_message.text = self.connector_func(self.last_message, f"Server #Railway#{self.railway_server_number} was stoped!")
                    self.run_flag = False
                    return
                # ///////////////// stop logic end /////////////////////////// 
                # ///////////////// ************* /////////////////////////// 
                # ///////////////// sleep logic //////////////////////////////  
                time_diff_seconds = self.work_sleep_manager(self.work_to, self.sleep_to)
                if time_diff_seconds:
                    self.last_message.text = self.connector_func(self.last_message, "It is time to rest! Let's go to bed!")        
                    time.sleep(time_diff_seconds)
                else:
                    if first_req_flag:
                        first_req_flag = False
                        self.last_message.text = self.connector_func(self.last_message, "It is time to work!")
                # ///////////////// sleep logic end /////////////////////////////
                # ///////////////// ***************** ///////////////////////////
                # ///////////////// pars logic //////////////////////////////////
                start_data = bg_parser.bitget_parser()
                if start_data:            
                    set_item = self.start_data_to_item(start_data) 
                    
                    try:
                        if set_item.get('listing_time_ms', None) > previous_set_item.get('listing_time_ms', None):
                            set_item = previous_set_item
                    except:
                        pass
                    self.listing_time_ms = set_item.get('listing_time_ms', None)  
                    # ///////////////// show set info logic /////////////////// 
                    show_counter += 1
                    if show_counter == 3:
                        self.last_message.text = self.connector_func(self.last_message, str(set_item))
                        show_counter = 0
                else:
                    self.last_message.text = self.connector_func(self.last_message, f"Server #Railway#{self.railway_server_number} pause2...")
                    # ///////////////// show set info logic end ///////////////////
                    time.sleep(random.randrange(239, 299)) 
                    # time.sleep(random.randrange(51, 61))
                    continue
                if self.listing_time_ms:
                    if self.left_time_in_minutes_func(self.listing_time_ms) <= 12:
                        if self.calibrator_flag:
                            self.delay_manager()
                        # ////////////////////////////////////////////////////////////////////// 
                        set_item.update(self.set_item)                   
                        self.last_message.text = self.connector_func(self.last_message, str(set_item)) 
                        # //////////////////////////////////////////////////////////////////////
                        db_connect_true = dbb_coordinator.db_connector()
                        if db_connect_true:
                            dbb_coordinator_repl = dbb_coordinator.db_writer(set_item) 
                            if dbb_coordinator_repl:
                                self.last_message.text = self.connector_func(self.last_message, 'Writing set_item data was making successfully!')
                            else:
                                self.last_message.text = self.connector_func(self.last_message, 'Some problems with writing set_item data...')
                        else:
                            self.last_message.text = self.connector_func(self.last_message, 'Some problem with db connecting...')
                        # cur_time = int(time.time()* 1000)
                        # total_log_instance.json_to_buffer('PARS', cur_time, start_data)                        
                        cur_time = int(time.time()* 1000)
                        total_log_instance.json_to_buffer('START', cur_time, [set_item]) 
                        json_file = total_log_instance.get_json_data()                
                        self.bot.send_document(self.last_message.chat.id, json_file)   
                        log_file = total_log_instance.get_logs()
                        self.bot.send_document(self.last_message.chat.id, log_file) 

                        set_item = {}  
                        time.sleep((self.listing_time_ms-int(time.time()*1000))/ 1000)                 
                        continue
                        # ////////////////////////////////////////////////////////////////////////////  
                else:
                    self.last_message.text = self.connector_func(self.last_message, "oops,... self.listing_time_ms == None")

                self.last_message.text = self.connector_func(self.last_message, f"Server #Railway#{self.railway_server_number} pause...")
                # print("pause...")
                time.sleep(random.randrange(239, 299))
                # time.sleep(random.randrange(51, 61)) 
        # ///////////////////////////////////////////////////////////////////////////////////
        self.last_message.text = self.connector_func(self.last_message, self.SOLI_DEO_GLORIA)

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
                            print(ex) 
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
                    print(ex)        

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
                        print(ex)
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
                    print(ex)
            # /////////////////////////////////////////////////////////////////////////////////////////////////////

            # self.bot.polling()
            self.bot.infinity_polling()
        except Exception as ex:
            print(ex)

if __name__=="__main__": 
    # pass #2  
    # MAIN_CONTROLLER().main_func() 
    print('Please go to the Telegram bot interface!')     
    bot = TG_MANAGER()   
    bot.run()

# git add . 
# git commit -m "betta15"
# git push -u origin master