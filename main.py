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
        response = self.place_market_order(symbol, 'BUY', self.depo)                
        response = response.json() 
        response['symbol'] = symbol
        response['side'] = 'BUY'
        response['status'] = 'filled'                           
        self.response_data_list.append(response)                   
        if response['msg'] == 'success': 
            print('buy success!')
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
            print('sell success!')   
            self.last_message.text = self.connector_func(self.last_message, 'sell success!') 
        else:                
            print(f"Symbol: {item['data'][0]['symbol']}:... some problems with placing the sell order") 
            self.last_message.text = self.connector_func(self.last_message, f"Symbol: {item['data'][0]['symbol']}:... some problems with placing the sell order")
                                         
    @log_exceptions_decorator        
    def extract_data_temp(self, item):            
        orderId = item['data']['orderId']           
        response_data = self.get_order_data(orderId)   
        response_data = response_data.json()                
        response_data['done'] = False
        response_data['real_price'] = float(response_data['data'][0]['quoteVolume'])/float(response_data['data'][0]['baseVolume'])                              
        response_data['qnt_to_sell_start'] = 0
        fills = response_data["data"]
        for fill in fills:
            try:
                response_data['qnt_to_sell_start'] += float(fill["baseVolume"])
            except:   
                pass   
        if response_data['qnt_to_sell_start'] > 10:   
            response_data['qnt_to_sell_start'] = int(response_data['qnt_to_sell_start']* 0.98)
        else:
            response_data['qnt_to_sell_start'] = round(response_data['qnt_to_sell_start']* 0.98, 2)
        if response_data['qnt_to_sell_start'] !=0:
            response_data['done'] = True
            item_copy = item.copy()
            item_copy.update(response_data)        
            self.response_data_list.append(item_copy)      
            de_qnt_to_sell_start = decimal.Decimal(str(item_copy['qnt_to_sell_start']))
            formatted_qnt_to_sell_start = format(de_qnt_to_sell_start, 'f')
            real_buy_price = decimal.Decimal(str(item_copy['real_price']))
            real_buy_price = format(real_buy_price, 'f')
            self.last_message.text = self.connector_func(self.last_message, f"qnt_to_sell_start {item_copy['symbol']}: {formatted_qnt_to_sell_start}" + '\n\n' + f"buy_price {item_copy['symbol']}: {real_buy_price}")
            print(f"qnt_to_sell_start {item_copy['symbol']}: {formatted_qnt_to_sell_start}")
            print(f"buy_price {item_copy['symbol']}: {real_buy_price}")  
        else:
            print(f"response_data['qnt_to_sell_start'] == 0") 

    @log_exceptions_decorator 
    def threads_executor_temp(self, arg_list, functionN):
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(arg_list)) as executor:
            executor.map(functionN, arg_list)

class MANAGER(TEMPLATES):
    def __init__(self) -> None:
        super().__init__()

    def delay_manager(self):
        def delay_calibrator(set_item):
            self.max_symbol_list_slice = 1
            good_test_flag = False     
            good_test_counter = 0
            retry_limit_counter = 6 
            # self.delay_time_ms = self.delay_default_time_ms           

            for i in range(retry_limit_counter):   
                try:         
                    if (good_test_counter == 2):                                            
                        return 1
                    elif not good_test_flag:
                        good_test_counter = 0
                    
                    self.last_message.text = self.connector_func(self.last_message, f"retry_counter_: {i}")
                    print(f"retry_counter_: {i}")
                    good_test_flag = False                  
                    if not self.trading_little_temp(set_item):
                        self.last_message.text = self.connector_func(self.last_message, 'Some problems with placing buy market orders on calibration step...' + '\n\n' + f"self.delay_time_ms: {self.delay_time_ms}")
                        print('Some problems with placing buy market orders on calibration step...')
                        print(f"self.delay_time_ms: {self.delay_time_ms}")
                        self.listing_time_ms += 60000
                        time.sleep(0.1)
                        continue
                    result_time_data_time, result_time_ms = self.show_trade_time_for_calibrator(self.response_data_list)
                    self.last_message.text = self.connector_func(self.last_message, result_time_data_time)
                    print(result_time_data_time)
                    if -4 <= result_time_ms - self.listing_time_ms <= 20:
                        good_test_flag = True
                        self.last_message.text = self.connector_func(self.last_message, f"good_test_flag: {str(good_test_flag)}")
                        print(f"good_test_flag: {good_test_flag}")
                        good_test_counter += 1
                    elif result_time_ms - self.listing_time_ms < -4:
                        self.last_message.text = self.connector_func(self.last_message, "self.listing_time_ms - result_time_ms < 4")
                        print("self.listing_time_ms - result_time_ms < 4")
                        self.delay_time_ms -= 7
                    elif result_time_ms - self.listing_time_ms > 20:
                        self.last_message.text = self.connector_func(self.last_message, "self.listing_time_ms - result_time_ms > 20")
                        print("self.listing_time_ms - result_time_ms > 20")
                        self.delay_time_ms += 7
                    
                    self.last_message.text = self.connector_func(self.last_message, f"self.delay_time_ms: {self.delay_time_ms}")
                    print(f"self.delay_time_ms: {self.delay_time_ms}")
                    self.listing_time_ms += 30000
                    time.sleep(0.1)
                except Exception as ex:
                    # print(f"main 117: {ex}")
                    self.last_message.text = self.connector_func(self.last_message, ex)
                    return 0
            return 1
        
        start_max_symbol_list_slice = self.max_symbol_list_slice
        self.max_symbol_list_slice = 1
        start_listing_time_ms = self.listing_time_ms
        start_depo = self.depo
        self.depo = 10
        start_data = [
            {
                "symbol_list": [self.default_test_symbol],
                "listing_time_ms": self.next_two_minutes_ms(),
                "listing_time": ""                        
            }
        ]        
        try:
            delay_manager_return = False
            set_item, self.listing_time_ms = self.params_gather(start_data, self.depo, self.delay_time_ms, self.default_params)
            delay_manager_return = delay_calibrator(set_item)
        except Exception as ex:
            print(ex)
        # self.threads_flag = start_threads_flag
        self.max_symbol_list_slice = start_max_symbol_list_slice
        self.depo = start_depo
        self.listing_time_ms = start_listing_time_ms
        if not delay_manager_return:
            self.last_message.text = self.connector_func(self.last_message, "Some problems with calibration...")
            print("Some problems with calibration...")
        self.trades_garbage()

    @log_exceptions_decorator
    def buy_manager(self, set_item):
        print("It is waiting time for buy!..")        
        self.last_message.text = self.connector_func(self.last_message, "It is waiting time for buy!...")
        self.response_data_list, self.response_success_list = [], [] 
        schedule_time_ms = self.listing_time_ms - 4000
        time.sleep((schedule_time_ms - int(time.time()*1000))/ 1000)             
        if not self.threads_flag:     
            buy_time_ms = self.listing_time_ms - self.delay_time_ms  
            try:              
                symbol = set_item["symbol_list"][self.symbol_list_el_position]  
            except Exception as ex:
                print(ex) 
                symbol = set_item["symbol_list"][0]               
            self.send_fake_request(self.symbol_fake) 
            time.sleep((buy_time_ms - int(time.time()*1000))/ 1000) 
            if self.pre_start_pause != 0:
                pre_start_increment = 0 if self.delay_time_ms == 0 else self.delay_time_ms/1000
                time.sleep(self.pre_start_pause + pre_start_increment)                  
            self.buy_market_temp(symbol)  
        else:
            set_item["symbol_list"] = set_item["symbol_list"][:self.max_symbol_list_slice]
            delay_upgrated = 0 if self.delay_time_ms == 0 else self.delay_time_ms + ((len(set_item["symbol_list"])-1)*119)            
            buy_time_ms = self.listing_time_ms - delay_upgrated if delay_upgrated != 0 else self.listing_time_ms
            symbol_list_for_fake_requests = [self.symbol_fake for _ in range(len(set_item["symbol_list"]))]
            self.threads_executor_temp(symbol_list_for_fake_requests, self.send_fake_request)
            time.sleep((buy_time_ms - int(time.time()*1000))/ 1000)  
            if self.pre_start_pause != 0:
                pre_start_increment = 0 if delay_upgrated == 0 else delay_upgrated/1000
                time.sleep(self.pre_start_pause + pre_start_increment)               
            self.threads_executor_temp(set_item["symbol_list"], self.buy_market_temp)               

    @log_exceptions_decorator   
    def sell_manager(self, set_item):
        if not self.threads_flag:
            self.extract_data_temp(self.response_success_list[0]) 
        else:                    
            self.threads_executor_temp(self.response_success_list, self.extract_data_temp)             
        # ///////////////////////////////////////////////////////
        if self.sell_mode == 't100':
            time.sleep(set_item["t100_mode_pause"])                    
            worker_list = []
            if all(not item.get('done', False) for item in self.response_data_list):
                self.last_message.text = self.connector_func(self.last_message, "Some problems with fetching trades data...")
                print("Some problems with fetching trades data...")
            else:
                for item in self.response_data_list:
                    if item.get('done'):                            
                        worker_list.append(item)  
                        if not self.threads_flag:                     
                            self.sell_market_temp(item)
                            break 

                if self.threads_flag:
                    self.threads_executor_temp(worker_list, self.sell_market_temp)

    def trading_little_temp(self, set_item):                                
        self.buy_manager(set_item)
        if len(self.response_success_list) != 0:
            self.sell_manager(set_item)        
        else:
            self.last_message.text = self.connector_func(self.last_message, 'Some problems with placing buy market orders...')
            print('Some problems with placing buy market orders...')             
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
        print(f'<<{self.market_place}>>')
        self.last_message.text = self.connector_func(self.last_message, f"Server #Railway#{self.symbol_list_el_position} <<{self.market_place}>>")
        show_counter = 0
        first_req_flag = True
        if self.controls_mode == 'a':  
            from info_pars import ANNONCEMENT             
            while True:
                start_data = []
                set_item = {}                
                if self.stop_flag:
                    self.last_message.text = self.connector_func(self.last_message, f"Server #Railway#{self.symbol_list_el_position} was stoped!")
                    return
                time_diff_seconds = self.work_sleep_manager(self.work_to, self.sleep_to)
                if time_diff_seconds:
                    self.last_message.text = self.connector_func(self.last_message, "It is time to rest! Let's go to bed!")        
                    time.sleep(time_diff_seconds)
                else:
                    if first_req_flag:
                        first_req_flag = False
                        self.last_message.text = self.connector_func(self.last_message, "It is time to work!")

                start_data = ANNONCEMENT().bitget_parser()
                # print(start_data)
                # log_file = total_log_instance.get_logs()
                # self.bot.send_document(self.last_message.chat.id, log_file) 
                if start_data:            
                    set_item, self.listing_time_ms = self.params_gather(start_data, self.depo, self.delay_time_ms, self.default_params)
                    show_counter += 1
                    if show_counter == 5:
                        self.last_message.text = self.connector_func(self.last_message, str(set_item))
                        show_counter = 0
                else:
                    self.last_message.text = self.connector_func(self.last_message, f"Server #Railway#{self.symbol_list_el_position} pause2...")
                    time.sleep(random.randrange(239, 299))
                    continue
                if self.left_time_in_minutes_func(self.listing_time_ms) <= 12:
                    if self.calibrator_flag:
                        self.delay_manager()
                    # //////////////////////////////////////////////////////////////////////
                    set_item["delay_time_ms"] = self.delay_time_ms
                    self.last_message.text = self.connector_func(self.last_message, str(set_item)) 
                    # //////////////////////////////////////////////////////////////////////
                    self.trading_little_temp(set_item) # main func
                    # //////////////////////////////////////////////////////////////////////                            
                    try:
                        cur_time = int(time.time()* 1000)
                        result_time, self.response_data_list = self.show_trade_time(self.response_data_list, 'bitget')                        
                        self.last_message.text = self.connector_func(self.last_message, result_time)
                        # print(result_time)  
                        cur_time = int(time.time()* 1000)
                        total_log_instance.json_to_buffer('PARS', cur_time, start_data)                        
                        cur_time = int(time.time()* 1000)
                        total_log_instance.json_to_buffer('START', cur_time, [set_item])  
                        cur_time = int(time.time()* 1000)
                        total_log_instance.json_to_buffer('TRADES', cur_time, self.response_data_list)   
                        json_file = total_log_instance.get_json_data()                
                        self.bot.send_document(self.last_message.chat.id, json_file)   
                        log_file = total_log_instance.get_logs()
                        self.bot.send_document(self.last_message.chat.id, log_file)       
                    except Exception as ex:
                        # message.text = self.connector_func(message, ex)
                        print(ex)

                    print("pause 30 sec...")   
                    time.sleep(30)
                    continue
                    # ////////////////////////////////////////////////////////////////////////////  
                self.last_message.text = self.connector_func(self.last_message, f"Server #Railway#{self.symbol_list_el_position} pause...")
                # print("pause...")
                time.sleep(random.randrange(239, 299)) 
                # time.sleep(random.randrange(9, 14)) 
        # ////////////////////////////////////////////////////////////   
        # print(self.SOLI_DEO_GLORIA)
        self.last_message.text = self.connector_func(self.last_message, self.SOLI_DEO_GLORIA)

class TG_MANAGER(MAIN_CONTROLLER):
    def __init__(self):
        super().__init__()  
        self.stop_redirect_flag = False  
        self.settings_redirect_flag = False    

    def run(self):  
        try:          
            @self.bot.message_handler(commands=['start'])
            @self.bot.message_handler(func=lambda message: message.text == 'START')
            def handle_start_input(message): 
                try:
                    self.stop_flag = False                           
                    response_message = 'God bless you Nik!'
                    print(response_message) 
                    self.bot.send_message(message.chat.id, response_message, reply_markup=self.menu_markup)
                    self.last_message = message
                    self.main_func()  
                except Exception as ex:
                    print(ex)              
                return 
            @self.bot.message_handler(func=lambda message: message.text == 'STOP')             
            def handle_stop(message):
                self.bot.send_message(message.chat.id, "Are you sure you want to stop the program? (y/n)")
                self.stop_redirect_flag = True

            @self.bot.message_handler(func=lambda message: self.stop_redirect_flag)             
            def handle_stop_redirect(message):
                self.stop_redirect_flag = False
                if message.text.strip().upper() == 'Y':
                    self.stop_flag = True 
                    self.bot.send_message(message.chat.id, "Please waiting...")                   
                else:
                    self.bot.send_message(message.chat.id, "Program was not stopped.")  

            @self.bot.message_handler(func=lambda message: message.text == 'SETTINGS')             
            def handle_settings(message):
                try:
                    message.text = self.connector_func(message, "Please enter a delay_ms and depo size using shift (e.g: 111 21)")
                    self.settings_redirect_flag = True
                except Exception as ex:
                    print(ex)

            @self.bot.message_handler(func=lambda message: self.settings_redirect_flag)             
            def handle_settings_redirect(message):
                try:
                    self.settings_redirect_flag = False
                    dataa = [x for x in message.text.strip().split(' ') if x.strip()]  
                    self.delay_time_ms = int(float(dataa[0]))   
                    self.depo = int(float(dataa[1]))
                    if len(dataa) == 2:     
                        message.text = self.connector_func(message, f"delay_time_ms: {self.delay_time_ms}\ndepo: {self.depo}")
                    else:
                        message.text = self.connector_func(message, f"Please enter a valid options...")
                except Exception as ex:
                    print(ex)

            # self.bot.polling()
            self.bot.infinity_polling()
        except Exception as ex:
            print(ex)

if __name__=="__main__":    
    print('Please go to the Telegram bot interface!')     
    bot = TG_MANAGER()   
    bot.run()

# git add . 
# git commit -m "betta15"
# git push -u origin master 
