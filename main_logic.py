import time
import random
from db_coordinator import DB_COOORDINATOR  

class TEMPLATES(DB_COOORDINATOR):
    def __init__(self) -> None:
        super().__init__()
        self.buy_market_temp = self.log_exceptions_decorator(self.buy_market_temp) 
        self.sell_market_temp = self.log_exceptions_decorator(self.sell_market_temp) 
        self.extract_data_temp = self.log_exceptions_decorator(self.extract_data_temp) 
    
    def buy_market_temp(self, symbol, depo):  
        response = self.place_market_order(symbol, 'BUY', depo)                
        response = response.json() 
        response['symbol'] = symbol
        response['side'] = 'BUY'
        response['status'] = 'filled'                           
        self.response_data_list.append(response)                   
        if response['msg'] == 'success': 
            self.handle_messagee('buy success!')
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
            self.handle_messagee('sell success!')  
        else:                
            self.handle_messagee(f"Symbol: {item['data'][0]['symbol']}:... some problems with placing the sell order")
            
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
            self.handle_exception(ex)

class MANAGER(TEMPLATES):
    def __init__(self) -> None:
        super().__init__()
        self.buy_manager = self.log_exceptions_decorator(self.buy_manager) 
        self.sell_manager = self.log_exceptions_decorator(self.sell_manager)
        self.trading_little_temp = self.log_exceptions_decorator(self.trading_little_temp) 
    
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
                self.handle_messagee("List index out of range. There is nothing to trade")
                time.sleep((buy_time_ms - int(time.time()*1000))/ 1000)
                return False
        # ///////////////////////////////////////////////////////////////////////////////// 
        tg_mess = f'symbol: {symbol}\ndepo: {set_item.get(f"depo_server{self.railway_server_number}", None)}\ndelay: {set_item.get(f"delay_time_ms_server{self.railway_server_number}", None)}\nlisting time: {set_item.get(f"listing_time_ms", None)}'
        self.handle_messagee(tg_mess + '\n' + "It is waiting time for buy!...")
        # ///////////////////////
        schedule_time_ms_1 = self.listing_time_ms - 15000
        time.sleep((schedule_time_ms_1 - int(time.time()*1000))/ 1000)  
        # /////////////////////////////////////// defencive mehanizm
        if self.is_order_book_defencive_meh:
            asks, bids = None, None
            order_book_data = self.get_order_book(symbol, limit=10)
            if order_book_data:
                asks, bids = order_book_data
                if asks or bids:
                    if not self.is_order_book_valid(asks, bids):
                        self.handle_messagee(f'{symbol} was skiped by is_order_book_valid func')
                        time.sleep((buy_time_ms - int(time.time()*1000))/ 1000)
                        return False
        # ////////////////////
        schedule_time_ms = self.listing_time_ms - 4000
        time.sleep((schedule_time_ms - int(time.time()*1000))/ 1000)  
        self.send_fake_request(self.symbol_fake)
        time.sleep((buy_time_ms - int(time.time()*1000))/ 1000)             
        self.buy_market_temp(symbol, set_item.get(f"depo_server{self.railway_server_number}", None))
        return True
       
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
                self.handle_messagee(f"Some problems with fetching trades data. Attempt number {i}")
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
        self.handle_messagee("All attempts to fetch trades data have failed." + '\n' + f"Failed to sell the {self.symbol} coin")           
    
    def trading_little_temp(self, set_item):                                
        if not self.buy_manager(set_item):
            return False
        if len(self.response_success_list) != 0:
            self.sell_manager(set_item)        
        else:
            self.handle_messagee('Some problems with placing buy market orders...')      
        return True
                        
class MAIN_CONTROLLER(MANAGER):
    def __init__(self) -> None:
        super().__init__()
        self.main_func = self.log_exceptions_decorator(self.main_func)

    def main_func(self): 
        self.run_flag = True 
        self.handle_messagee(f"Server #Railway#{self.railway_server_number} <<{self.market_place}>>") 
        show_counter = 0
        first_req_flag = True

        while True:
            set_item = {} 
            self.listing_time_ms = None               
            if self.stop_flag:
                self.handle_messagee(f"Server #Railway#{self.railway_server_number} was stoped!") 
                self.run_flag = False
                return
            time_diff_seconds = self.work_sleep_manager(self.work_to, self.sleep_to)
            if time_diff_seconds:
                self.handle_messagee("It is time to rest! Let's go to bed!")     
                time.sleep(time_diff_seconds)
                continue
            else:
                if first_req_flag:
                    first_req_flag = False
                    self.handle_messagee("It is time to work!")
            try:
                if self.db_connector():
                    db_reading_data = None
                    db_reading_data = self.read_db_data()
       
                    if db_reading_data:
                        self.listing_time_ms, set_item = self.formate_db_data(db_reading_data)
                        # self.handle_messagee(f"{self.listing_time_ms},\n{set_item}")
                else:
                    self.handle_messagee(f"Server #Railway#{self.railway_server_number} some problems with db connecting...")

                if set_item and self.listing_time_ms:            
                    show_counter += 1
                    if show_counter == 15:
                        if 0 < self.left_time_in_minutes_func(self.listing_time_ms):

                            symbol_list = set_item.get('symbol_list', 'No symbol list available')
                            listing_time = set_item.get('listing_time', 'No listing time available')
                            delay_time = set_item.get(f'delay_time_ms_server{self.railway_server_number}', 'No delay data available')
                            depo_data = set_item.get(f'depo_server{self.railway_server_number}', 'No depo data available')

                            message = (
                                f"Symbol List: {symbol_list}\n"
                                f"Listing Time: {listing_time}\n"
                                f"Delay Time (Server {self.railway_server_number}): {delay_time}\n"
                                f"Depo Data (Server {self.railway_server_number}): {depo_data}"
                            )

                            self.handle_messagee(message)

                        else:
                            self.handle_messagee("There is no trading data at the current moment!..")
                        show_counter = 0
                else:
                    time.sleep(random.randrange(59, 69))
                    continue
            except Exception as ex:
                self.handle_exception(ex)

            if 0 < self.left_time_in_minutes_func(self.listing_time_ms) <= 3:
                try:
                    # //////////////////////////////////////////////////////////////////////
                    if not self.trading_little_temp(set_item):
                        self.response_data_list = []
                        self.listing_time_ms = None
                        continue
                    # //////////////////////////////////////////////////////////////////////          
                    # cur_time = int(time.time()* 1000)
                    result_time, self.response_data_list = self.show_trade_time(self.response_data_list, 'bitget')
                    self.handle_messagee(result_time)
                    # self.handle_messagee(self.from_json_to_string_formeter(self.response_data_list))       
                except Exception as ex:
                    self.handle_exception(ex)

                time.sleep(30)
                continue

            time.sleep(random.randrange(59, 69)) 

