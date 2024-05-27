# import decimal
import time
import random
from utils import UTILS
from tg_connector import TG_CONNECTOR 
from db_coordinator import DB_COOORDINATOR  
from log import total_log_instance, log_exceptions_decorator

class TEMPLATES(TG_CONNECTOR, UTILS):
    def __init__(self) -> None:
        super().__init__()
        self.symbol = None

    @log_exceptions_decorator
    def message_template(self, textt):
        print(textt)
        if self.last_message:
            if textt:
                self.last_message.text = self.connector_func(self.last_message, str(textt))
                return
            self.last_message.text = self.connector_func(self.last_message, "Opss... text data is empty!")
    
    @log_exceptions_decorator
    def buy_market_temp(self, symbol, depo):  
        response = self.place_market_order(symbol, 'BUY', depo)                
        response = response.json() 
        response['symbol'] = symbol
        response['side'] = 'BUY'
        response['status'] = 'filled'                           
        self.response_data_list.append(response)                   
        if response['msg'] == 'success': 
            self.message_template('buy success!')
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
            self.message_template('sell success!')  
        else:                
            self.message_template(f"Symbol: {item['data'][0]['symbol']}:... some problems with placing the sell order")

    @log_exceptions_decorator        
    def extract_data_temp(self, item):            
        orderId = item.get('data', None).get('orderId', None)
        if orderId is not None:    
            response_data = self.get_order_data(orderId).json()
        else:
            return
        # self.message_template(response_data)
        response_data['done'] = False
        response_data['qnt_to_sell_start'] = 0
        response_data['real_price'] = 0
        
        try:
            fills = response_data.get("data", [])            
            base_volume = sum(float(fill.get("baseVolume", 0)) for fill in fills)
            # quote_volume = sum(float(fill.get("quoteVolume", 0)) for fill in fills)
            
            if base_volume >= 10:
                response_data['qnt_to_sell_start'] = int(base_volume * 0.98)
            elif 1 < base_volume < 10:
                response_data['qnt_to_sell_start'] = int(base_volume)
            else:
                response_data['qnt_to_sell_start'] = round(base_volume * 0.98, 4)
            
            if response_data['qnt_to_sell_start'] != 0:
                response_data['done'] = True
                item_copy = item.copy()
                item_copy.update(response_data)      
                self.response_data_list.append(item_copy) 
        except Exception as ex:
            self.message_template(ex)

class MANAGER(TEMPLATES):
    def __init__(self) -> None:
        super().__init__()

    @log_exceptions_decorator
    def buy_manager(self, set_item):
        symbol = None
        self.response_data_list, self.response_success_list = [], []
        buy_time_ms = self.listing_time_ms - set_item.get(f"delay_time_ms_server{self.railway_server_number}", None)      
        try:              
            self.symbol = symbol = set_item["symbol_list"][1]  
        except Exception as ex:
            # print(ex) #
            if self.trade_duble_flag:
                self.symbol = symbol = set_item["symbol_list"][0]  
            else:
                self.message_template("List index out of range. There is nothing to trade")
                return  
        # ///////////////////////////////////////////////////////////////////////////////// 
        tg_mess = f'symbol: {symbol}\ndepo: {set_item.get(f"depo_server{self.railway_server_number}", None)}\ndelay: {set_item.get(f"delay_time_ms_server{self.railway_server_number}", None)}\nlisting time: {set_item.get(f"listing_time_ms", None)}'
        self.message_template(tg_mess)
        self.message_template("It is waiting time for buy!...")
        # /////////////////////////////////////////////////////////////////////////////////  
        schedule_time_ms = self.listing_time_ms - 4000
        time.sleep((schedule_time_ms - int(time.time()*1000))/ 1000)  
        self.send_fake_request(self.symbol_fake) 
        time.sleep((buy_time_ms - int(time.time()*1000))/ 1000)             
        self.buy_market_temp(symbol, set_item.get(f"depo_server{self.railway_server_number}", None))            
  
    @log_exceptions_decorator   
    def sell_manager(self, set_item):
        # Получаем значение задержки из set_item с использованием значения по умолчанию 1.6
        time_duration = set_item.get(f"t100_mode_pause_server{self.railway_server_number}", 1.6)
        # Проверяем, является ли полученное значение числом с плавающей точкой
        if not isinstance(time_duration, float):
            time_duration = 1.6

        # Ждем половину времени задержки
        time.sleep(time_duration / 2)

        # Делаем две попытки
        for i in range(1, 3):
            # Извлекаем временные данные
            self.extract_data_temp(self.response_success_list[0])

            # Проверяем, все ли элементы списка response_data_list не выполнены
            if all(not item.get('done', False) for item in self.response_data_list):
                self.message_template(f"Some problems with fetching trades data. Attempt number {i}")
                continue
            else:
                # Если есть выполненные элементы, обрабатываем их
                for item in self.response_data_list:
                    if item.get('done'):
                        # Если это первая попытка, ждем половину времени задержки
                        time_duration = time_duration / 2 if i == 1 else 0
                        time.sleep(time_duration)
                        # Продаем
                        self.sell_market_temp(item)
                        break
                return
        # Если ни одна из попыток не удалась
        self.message_template("All attempts to fetch trades data have failed.")
        self.message_template(f"Failed to sell the {self.symbol} coin")
                
    @log_exceptions_decorator
    def trading_little_temp(self, set_item):                                
        self.buy_manager(set_item)
        if len(self.response_success_list) != 0:
            self.sell_manager(set_item)        
        else:
            self.message_template('Some problems with placing buy market orders...')      
        return True
                        
class MAIN_CONTROLLER(MANAGER):
    def __init__(self) -> None:
        super().__init__()

    def main_func(self): 
        self.run_flag = True 
        dbb = DB_COOORDINATOR(self.db_host, self.db_port, self.db_user, self.db_password, self.db_name)
        self.message_template(f"Server #Railway#{self.railway_server_number} <<{self.market_place}>>") 
        show_counter = 0
        first_req_flag = True
        # ////////////////////////////////////////////////////////////////////////
        while True:
            set_item = {} 
            self.listing_time_ms = None               
            if self.stop_flag:
                self.message_template(f"Server #Railway#{self.railway_server_number} was stoped!") 
                self.run_flag = False
                return
            time_diff_seconds = self.work_sleep_manager(self.work_to, self.sleep_to)
            if time_diff_seconds:
                self.message_template("It is time to rest! Let's go to bed!")     
                time.sleep(time_diff_seconds)
                continue
            else:
                if first_req_flag:
                    first_req_flag = False
                    self.message_template("It is time to work!")
            try:
                if dbb.db_connector():
                    db_reading_data = None
                    db_reading_data = dbb.read_db_data()
                    # self.message_template(db_reading_data)
                    if db_reading_data:
                        self.listing_time_ms, set_item = dbb.formate_db_data(db_reading_data)
                        # self.message_template(f"{self.listing_time_ms},\n{set_item})
                else:
                    self.message_template(f"Server #Railway#{self.railway_server_number} some problems with db connecting...")

                if set_item and self.listing_time_ms:            
                    show_counter += 1
                    if show_counter == 15:
                        if 0 < self.left_time_in_minutes_func(self.listing_time_ms):
                            self.message_template(f"symbol_list: {set_item.get('symbol_list', 'No symbol list available')}\nlisting_time: {set_item.get('listing_time', 'No listing time available')}\ndelay_time_ms_server{self.railway_server_number}: {set_item.get(f'delay_time_ms_server{self.railway_server_number}', 'No delay data available')}\ndepo_server{self.railway_server_number}: {set_item.get(f'depo_server{self.railway_server_number}', 'No depo data available')}")
                        else:
                            self.message_template("There is no trading data at the current moment!..")
                        show_counter = 0
                else:
                    time.sleep(random.randrange(59, 69))
                    continue
            except Exception as ex:
                self.message_template(ex)

            if 0 < self.left_time_in_minutes_func(self.listing_time_ms) <= 3:
                try:
                    # //////////////////////////////////////////////////////////////////////
                    self.trading_little_temp(set_item) # main func
                    # //////////////////////////////////////////////////////////////////////          
                    cur_time = int(time.time()* 1000)
                    result_time, self.response_data_list = self.show_trade_time(self.response_data_list, 'bitget')
                    self.message_template(result_time)                        
                    cur_time = int(time.time()* 1000)
                    total_log_instance.json_to_buffer('TRADES', cur_time, self.response_data_list)   
                    json_file = total_log_instance.get_json_data()                
                    self.bot.send_document(self.last_message.chat.id, json_file)   
                    log_file = total_log_instance.get_logs()
                    self.bot.send_document(self.last_message.chat.id, log_file)    
                except Exception as ex:
                    self.message_template(ex)

                print("pause 30 sec...")   
                time.sleep(30)
                continue
                # ////////////////////////////////////////////////////////////////////////////
            # print("pause...")
            time.sleep(random.randrange(59, 69)) 

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
                self.last_message = message
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
            # self.bot.polling()
            self.bot.infinity_polling()
        except Exception as ex: 
            print(ex)

if __name__=="__main__": 
    # print('Server2 is refactoring')   
    # MAIN_CONTROLLER().main_func()
    print('Please go to the Telegram bot interface!')     
    bot = TG_MANAGER()   
    bot.run()