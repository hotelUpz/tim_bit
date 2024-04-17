    # def get_start_of_day(self):
    #     # now = datetime.datetime.now()
    #     # start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    #     now = datetime.datetime.now()
    #     start_of_day = datetime.datetime(now.year, now.month, now.day)
    #     return int(start_of_day.timestamp() * 1000)  # Convert to Unix milliseconds
    #  GET //////////////////////////////////////////////////////////////////
    # def create_session(self):
    #     url = f"https://api.binance.com/api/v3/exchangeInfo?symbol={self.symbol}"
    #     print(self.session.get(url)) 


    # def m_mode(self, qnt_to_sell_start, response_data_list):
    #     left_qnt = qnt_to_sell_start
    #     stop_selling = False                
    #     qnt_percent_pieces_left = 100
    #     while True:
    #         if not stop_selling:
    #             qnt_percent_pieces = input(f"Are you sure you want to sell {self.symbol}? If yes, tub a pieces qty (%) (e.g.: 1-100). Opposite tub enithing else for exit",)  
    #             try:                                      
    #                 qnt_percent_pieces = int(qnt_percent_pieces.strip())
    #                 qnt_percent_pieces_left = qnt_percent_pieces_left - qnt_percent_pieces
    #                 if qnt_percent_pieces_left < 0:
    #                     qnt_percent_pieces_left = qnt_percent_pieces_left + qnt_percent_pieces
    #                     print(f'Please enter a valid data. There are {qnt_percent_pieces_left} pieces left to sell')
    #                     continue                              
    #             except:
    #                 print('Selling session was deprecated. Have a nice day!')
    #                 return response_data_list
    #             try:
    #                 stop_selling = qnt_percent_pieces_left == 0        
    #                 qnt_multipliter = qnt_percent_pieces/100
    #                 qnt_to_sell = int(qnt_to_sell_start* qnt_multipliter)                           
    #                 print(f"qnt_to_sell: {qnt_to_sell}")
    #                 response_data_list_item, sell_success_flag = self.sell_market_temp(qnt_to_sell)
    #                 response_data_list += response_data_list_item  
    #                 self.json_writer(self.symbol, response_data_list)
    #                 if sell_success_flag:
    #                     left_qnt = left_qnt - qnt_to_sell  
    #                 else:
    #                     qnt_percent_pieces_left = qnt_percent_pieces_left + qnt_percent_pieces
    #                 print(f"Trere are {qnt_percent_pieces_left} pieces and {left_qnt} qty left to sell")                       
    #             except Exception as ex:                
    #                 logging.exception(
    #                     f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")                                   
    #             continue
    #         return response_data_list

        # self.set_list = [
        #     {
        #         "market_place": "bitget",
        #         "symbol_list": [
        #             "ARBUSDT",
        #             "TONCOINUSDT"
  
        #         ],
        #         "depo": 9,
        #         "sell_mode": "t100",
        #         "pre_starting_flag": 1,
        #         "decriment_time_ms": 146,
        #         "incriment_time_ms": 1,
        #         "pre_start_pause": 0,
        #         "t100_mode_pause_list": [
        #             0.9,
        #             1.9,
        #         ],
        #         "listing_time_ms": "",
        #         "listing_time": "2024-03-22 03:26:00",
        #         "link_list": [
        #         ]
        #     }
        # ]


# left_time_to_lunch_organizer = set_list[0]["listing_time_ms"] - 300000 - int(time.time()* 1000)
# print(f"left_time_to_lunch_organizer: {round(left_time_to_lunch_organizer/60000, 2)} min")
# await asyncio.sleep(left_time_to_lunch_organizer)  


# import random
# for _ in range(10):
#     print(random.randrange(8,21)/10)
# [1710844616000, 1710844619871, 1710844619871, 1710844620142]
# 1710845399870, 1710845400317
# data = '2024-03-18 12:00:00'
# params = {
#     'symbol': 'ETHFIUSDT',
#     'side': 'BUY',
#     'quoteOrderQty': 14,
#     'timestamp': 1710763200001
# }
# ошибка:
#     {
#         "code": -2010,
#         "msg": "Filter failure: LOT_SIZE"
#     }

# good_list = [(1,2), (3,7), (5,6)]
# print(sorted(good_list, key=lambda x: x[1], reverse=False))
# [{'code': '00000', 'msg': 'success', 'requestTime': 1711198621458, 'data': [{'userId': '5604086735', 'symbol': 'ARBUSDT', 'orderId': '1155416245652594689', 'clientOid': '0422eaca-3c24-4503-bba9-7e70d2210b8c', 'price': '0', 'size': '11', 'orderType': 'market', 'side': 'buy', 'status': 'filled', 'priceAvg': '1.6137000000000000', 'baseVolume': '6.81', 'quoteVolume': '10.9892970000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.00681,"t":-0.00681,"totalDeductionFee":0},"ARB":{"deduction":false,"feeCoinCode":"ARB","totalDeductionFee":0,"totalFee":-0.0068100000000000}}', 'orderSource': 'market', 'cTime': '1711198620236', 'uTime': '1711198620359'}], 'symbol': 'ARBUSDT', 'side': 'BUY', 'status': 'filled', 'done': True, 'real_price': 1.6137000000000001, 'qnt_to_sell_start': 6}]
 

                # with concurrent.futures.ThreadPoolExecutor(max_workers=len_symbol_list) as executor:
                #     executor.map(self.buy_market_temp, symbol_list)

                # print(self.response_success_list)
                # with concurrent.futures.ThreadPoolExecutor(max_workers=len_symbol_list) as executor:
                #     executor.map(self.extract_data_temp, self.response_success_list)

                # with concurrent.futures.ThreadPoolExecutor(max_workers=len_symbol_list) as executor:
                #     executor.map(self.sell_market_temp, worker_list)

# extract_data_done_counter = sum(1 for x in self.response_data_list if x.get('done'))

# import concurrent.futures

# class TEMPLATES(BITGET_API, UTILS):
#     def __init__(self) -> None:
#         super().__init__()
#         self.lock_response_data = threading.Lock()
    
#     def total_threads_executor(self, arg_list, functionN):
#         with concurrent.futures.ThreadPoolExecutor(max_workers=len(arg_list)) as executor:
#             futures = {executor.submit(functionN, item, i): (item, i) for i, item in enumerate(arg_list)}
#             for future in concurrent.futures.as_completed(futures):
#                 _, i = futures[future]
#                 try:
#                     future.result()
#                 except Exception as e:
#                     logging.exception(f"Thread execution failed: {e}")


    
    # def nex_minute_ms(self):
    #     return ((int(time.time() * 1000) + 59999) // 60000) * 60000 

    # def price_precession_extractor(self, enter_price):
    #     from decimal import Decimal        
    #     try:
    #         step_size = str(enter_price)      
    #         price_precision = Decimal(step_size).normalize().to_eng_string()    
    #         return len(price_precision.split('.')[1])          
    #     except Exception as ex:            
    #         logging.exception(
    #             f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
    #         return 1


                # if self.calibrator_flag:                    
                #     if set_item["listing_time_ms"] - int(time.time()* 1000) > 900000 and set_item["listing_time_ms"] - int(time.time()* 1000) < 1200000:                        
                #         self.dalay_manager()
                        
                # if set_item["listing_time_ms"] - int(time.time()* 1000) < 600000 and set_item["listing_time_ms"] - int(time.time()* 1000) > 0:
                #     # ////////////////////////////////
                #     self.trading_little_temp(set_item)
                #     # ////////////////////////////////


    # def from_string_to_date_time(self, date_time_str):
    #     try:
    #         pattern = r'(\d{1,2})(?:st|nd|rd|th) (\w+) (\d{4}), (\d{1,2}):(\d{2}) \(UTC\)'
    #         match = re.match(pattern, date_time_str)

    #         if match:            
    #             day = int(match.group(1))
    #             month_str = match.group(2)
    #             year = int(match.group(3))
    #             hour = int(match.group(4))
    #             minute = int(match.group(5))
    #             months = {
    #                 'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
    #                 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
    #             }
    #             month = months.get(month_str)
    #             if month:
    #                 dt = dttm(year, month, day, hour, minute)
    #                 milliseconds = int(dt.timestamp() * 1000)
    #                 return milliseconds
    #         return
    #     except Exception as ex:
    #         logging.exception(
    #             f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
    #         return

    # def symbol_extracter(self, text):    
    #     matches = re.findall(r'\((.*?)\)', text)
    #     extracted_text = [re.sub(r'[\(\)\.,\-!]', '', match) for match in matches]
    #     return extracted_text

    # def set_list_formator(self, find_data):
    #     import random
    #     try:
    #         unik_time_set = {x["listing_time_ms"] for x in find_data}
    #         unik_time_list = sorted(list(unik_time_set))
    #         new_data = []
    #         for time_ms in unik_time_list:
    #             data_item = {
    #                 "symbol_list": [],
    #                 "delay_time_ms": "",
    #                 "t100_mode_pause": random.randrange(12, 21) / 10,
    #                 "listing_time_ms": None,
    #                 "listing_time": ""
    #             }
    #             for item in find_data:
    #                 if item["listing_time_ms"] == time_ms:
    #                     data_item["symbol_list"].extend(item["symbol_list"])
    #                     data_item["listing_time_ms"] = item["listing_time_ms"]
    #                     data_item["listing_time"] = item["listing_time"]
    #             new_data.append(data_item)
    #         return new_data
    #     except Exception as ex:
    #         logging.exception(
    #             f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")
    #         return []

    
    # def set_list_formator(self, find_data):
    #     import random
    #     try:
    #         unik_time_set = set()
    #         unik_time_list = []
    #         for x in find_data:
    #             unik_time_set.add(x["listing_time_ms"])
    #         unik_time_list = sorted(list(unik_time_set), reverse=False)                             
    #         new_data = [
    #                         {                                
    #                             "symbol_list": [],                                
    #                             "delay_time_ms": "",
    #                             "t100_mode_pause": random.randrange(12,21)/10,
    #                             "listing_time_ms": None, 
    #                             "listing_time": "",                                                             
    #                         }
    #                     for _ in range(len(unik_time_list))
    #                     ]  
                        
    #         for j, y in enumerate(unik_time_list):
    #             for _, x in enumerate(find_data):
    #                 if x["listing_time_ms"] == y: 
    #                     try:                           
    #                         new_data[j]["symbol_list"] += x["symbol_list"]   
    #                         new_data[j]["listing_time_ms"] = x["listing_time_ms"]  
    #                         new_data[j]["listing_time"] = x["listing_time"]                          
    #                     except Exception as ex:                                          
    #                         logging.exception(
    #                             f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}")

    #         return new_data 
    #     except Exception as ex:                                          
    #         logging.exception(
    #             f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
    #         return [] 


# import requests
# from bs4 import BeautifulSoup
# from joblib import Parallel, delayed
# import time
# from random import choice
# from utils import UTILS
# import logging, os, inspect
# logging.basicConfig(filename='log.log', level=logging.INFO)
# current_file = os.path.basename(__file__) 

# time_correction = 10800000
# # time_correction = 7600000

# user_agents = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
# ]

# bitget_headers = {
#     'authority': 'www.bitget.com',    
#     'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
#     'origin': 'https://www.bitget.com/',
#     'referer': 'https://www.bitget.com/',
#     'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
#     'sec-ch-ua-mobile': '?0',    
#     'sec-fetch-dest': 'script',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'cross-site',
#     'User-Agent': ""
# }

# class ANNONCEMENT(UTILS):
#     def __init__(self) -> None:
#         super().__init__() 
#         self.session = requests.Session() 
#         self.session.mount('https://www.bitget.com', requests.adapters.HTTPAdapter(pool_connections=20, pool_maxsize=20))

#     def links_multiprocessor(self, links_bunch, cur_time, cpu_count=9): 
#         try:
#             total_list = []
#             # Используем lambda для создания анонимной функции с предопределенным аргументом cur_time
#             res = Parallel(n_jobs=cpu_count, prefer="threads")(delayed(lambda item: self.bitget_links_handler(item, cur_time))(item) for item in links_bunch)
#             for x in res: 
#                 if x:               
#                     try:                    
#                         total_list += x 
#                     except:
#                         pass 
#             return total_list
#         except Exception as ex:                    
#             logging.exception(
#                 f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
#             return total_list 
    
#     def bitget_links_handler(self, link, cur_time):
#         data_set = []
#         bitget_headers['User-Agent'] = choice(user_agents)
#         try:
#             r = self.session.get(url=link, headers=bitget_headers)
#             soup = BeautifulSoup(r.text, 'lxml')
#             listing_time_date_string = soup.find('div', class_='ArticleDetails_actice_details_main__oIjfu').find_all('p')[3].get_text().strip().split(': ')[1].strip()           
#             listing_time = self.from_string_to_date_time(listing_time_date_string)            
#             if listing_time > cur_time - time_correction:
#                 title = soup.find('h1').get_text().strip()        
#                 symbol_data = self.symbol_extracter2(title)                
#                 if symbol_data:
#                     symbol_list = []                                       
#                     for x in symbol_data:
#                         symbol_list.append(x.strip() + 'USDT')                        
#                     data_set.append(
#                         {                                
#                             "symbol_list": symbol_list,                                
#                             "listing_time_ms": listing_time + time_correction, 
#                             "listing_time": self.milliseconds_to_datetime_for_parser(listing_time + 21600000),
#                             "link": link             
#                         }
#                     )                        
#                 return data_set
#         except Exception as ex: 
#             return [] 
                       
#     def bitget_parser(self):        
#         try:
#             print('Start parser')
#             start_time = self.get_start_of_day()
#             url = f"https://api.bitget.com/api/v2/public/annoucements?&annType=coin_listings&language=en_US"        
#             data = self.session.get(url).json()["data"]
#             data = [{**x, "cTime": int(float(x["cTime"]))} for x in data if int(float(x["cTime"])) > start_time]                      
#             data = sorted(data, key=lambda x: x["cTime"], reverse=True)    
#             print(data)        
#             links_bunch = [x["annUrl"] for x in data]
#             links_bunch = list(set(links_bunch))            
#             cur_time = int(time.time()* 1000)
#             find_data = self.links_multiprocessor(links_bunch, cur_time) 
#             # return sorted(find_data, key=lambda x: x["listing_time_ms"], reverse=True) 
#             da = sorted(find_data, key=lambda x: x["listing_time_ms"], reverse=True) 
#             target = 'PARS'            
#             self.json_writer(da, target, cur_time+time_correction) 
#             return da
#         except Exception as ex:                    
#             logging.exception(
#                 f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
            
# print(ANNONCEMENT().bitget_parser()) 


    # def symbol_extracter2(self, text):       
    #     for x in text.split(' '):
    #         new_x = x.replace('.', '')
    #         if  new_x[0] == '(' and new_x[-1] == ')': 
    #             return [new_x[1:-1]]               
    #     return None

    # def from_string_to_date_time2(self, date_time_str):
    #     # '''2nd April 2024, 11:00 (UTC)'''
    #     try:
    #         matches = [x for x in date_time_str.strip().split(' ') if x.strip()]
    #         if matches:            
    #             day = int(re.match(r'\d+', matches[0]).group())
    #             month_str = matches[1].capitalize()
    #             year = int(re.match(r'\d+', matches[2]).group())
    #             hour = int(matches[3].split(':')[0])
    #             minute = int(matches[3].split(':')[1])
    #             months = {
    #                 'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
    #                 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
    #             }
    #             month = months.get(month_str)
    #             if month:
    #                 dt = dttm(year, month, day, hour, minute)
    #                 milliseconds = int(dt.timestamp() * 1000)
    #                 return milliseconds
    #         return
    #     except Exception as ex:
    #         logging.exception(
    #             f"An error occurred in file '{current_file}', line {inspect.currentframe().f_lineno}: {ex}") 
    #         return

# data = sorted(data, key=lambda x: x["cTime"], reverse=True)



    # def get_logs_from_database(self, timedelta_stamps, timedelta_stamps_value):
    #     session = self.Session()
    #     end_time = datetime.utcnow()
    #     start_time = end_time - timedelta(hours=timedelta_stamps_value)
    #     logs = session.query(Log).filter(Log.timestamp >= start_time, Log.timestamp <= end_time).all()
    #     session.close()
    #     return logs

# from sqlalchemy import create_engine, Column, Integer, String, DateTime



# class TestClass():
#     def __init__(self):
#         super().__init__()

#     @log_exceptions_decorator
#     def example_function(self):
#         x = 1 / 0

# if __name__ == "__main__":
#     test_instance = TestClass()

#     log_instance.flush_logs_to_database()    
#     timedelta_stamps = 'minutes'
#     timedelta_stamps_value = 1
#     logs = log_instance.get_logs_from_database(timedelta_stamps, timedelta_stamps_value)
#     for log in logs:
#         print(f"Timestamp: {log.timestamp}, File: {log.file_name}, Line: {log.line_number}, Message: {log.exception_message}")


# # class TestClass(Logger):
#     def __init__(self):
#         super().__init__()

#     def example_function(self):
#         x = 1 / 0

# if __name__ == "__main__":
#     test_instance = TestClass()
#     test_instance.example_function = test_instance.log_exceptions_decorator(test_instance.example_function)

#     for i in range(2):
#         test_instance.example_function()

#     test_instance.flush_logs_to_database()
#     # timedelta_stamps = 'days'
#     # timedelta_stamps = 'hours'
#     timedelta_stamps = 'minutes'
#     # timedelta_stamps = 'seconds'
#     timedelta_stamps_value = 1
#     logs = test_instance.get_logs_from_database(timedelta_stamps, timedelta_stamps_value)
#     for log in logs:
#         print(f"Timestamp: {log.timestamp}, File: {log.file_name}, Line: {log.line_number}, Message: {log.exception_message}")



# class Log(Logger.Base):
#     __tablename__ = 'logs'
#     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
#     timestamp = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow)
#     file_name = sqlalchemy.Column(sqlalchemy.String)
#     line_number = sqlalchemy.Column(sqlalchemy.Integer)
#     exception_message = sqlalchemy.Column(sqlalchemy.String)
# # ////////////////////////////////////////////////////////////
# class JsonData(Logger.Base):
#     __tablename__ = 'json_data'

#     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
#     target = sqlalchemy.Column(sqlalchemy.String)
#     cur_time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow)
#     data = sqlalchemy.Column(sqlalchemy.String)


    # @log_exceptions_decorator
    # def json_writer(self, data, target, cur_time):
    #     time_lable = self.milliseconds_to_datetime_for_parser(cur_time+time_correction)
    #     time_lable = time_lable.replace(':','_').replace(' ', '__')
    #     with open(f"BITGET_{target}_DATA/{time_lable}.json", "w") as f:
    #         json.dump(data, f, indent=4)


    # # ////////////////////////////////////////////////////////////////////////////////
    # def json_writer(self, data, target, cur_time):
    #     json_data = json.dumps(data)
    #     json_entry = JsonData(target=target, cur_time=cur_time, data=json_data)
    #     session = self.Session()
    #     session.add(json_entry)
    #     session.commit()
    #     session.close()

    
    # def logs_fetchData_temp(self, timedelta_stamps, timedelta_stamps_value):
    #     self.flush_logs_to_database() 
    #     logs = self.get_logs_from_database(timedelta_stamps, timedelta_stamps_value)
    #     for log in logs:
    #         print(f"Timestamp: {log.timestamp}, File: {log.file_name}, Line: {log.line_number}, Message: {log.exception_message}")



        # # Отправляем файл в Telegram
        # # bot.send_document(chat_id=chat_id, document=file)

    
    # def logs_fetchData_temp(self, timedelta_stamps, timedelta_stamps_value):
    #     self.flush_logs_to_database() 
    #     logs = self.get_logs_from_database(timedelta_stamps, timedelta_stamps_value)
    #     for log in logs:
    #         print(f"Timestamp: {log.timestamp}, File: {log.file_name}, Line: {log.line_number}, Message: {log.exception_message}")


# db_url='sqlite:///logs.db'




            # @self.bot.message_handler(func=lambda message: message.text == 'LOG')
            # def handle_get_log(message):                
            #     log_file = total_log_instance.get_logs()
            #     try:                   
            #         self.bot.send_document(message.chat.id, log_file)
            #     except:
            #         pass
            #     return            
            # @self.bot.message_handler(func=lambda message: message.text == 'JSON_DATA')
            # def handle_get_json(message):                
            #     json_file = total_log_instance.get_json_data()
            #     try:                   
            #         self.bot.send_document(message.chat.id, json_file)
            #     except:
            #         pass
            #     return


    # MAIN_CONTROLLER().main_func()




                # response_message = "Please wait..."
                # message.text = self.connector_func(message, response_message)
                # return
                    # response_message = "Please wait..."
                # message.text = self.connector_func(message, response_message)



        # if self.controls_mode == 'a':  
        #     from info_pars import ANNONCEMENT
        #     delay_true = False             
        #     while True:
        #         if self.stop_flag:
        #             self.last_message.text = self.connector_func(self.last_message, "The pogramm was stoped!")
        #             return
        #         self.work_sleep_manager(self.work_to, self.sleep_to)
        #         start_data = ANNONCEMENT().bitget_parser() 
        #         # //////////////////////////////////////////////////////////////////////////////////////
        #         if start_data:            
        #             set_item, self.listing_time_ms = self.params_gather(start_data, self.delay_time_ms, self.default_params) 
        #             print(set_item)                                   
        #             self.last_message.text = self.connector_func(self.last_message, str(set_item))                                         
        #             try:
        #                 cur_time = int(time.time()* 1000)
        #                 total_log_instance.json_to_buffer('PARS', cur_time, start_data)                        
        #                 cur_time = int(time.time()* 1000)
        #                 set_item_for_write = [set_item]
        #                 total_log_instance.json_to_buffer('START', cur_time, set_item_for_write)  
        #                 json_file = total_log_instance.get_json_data()                
        #                 self.bot.send_document(self.last_message.chat.id, json_file)   
        #                 log_file = total_log_instance.get_logs()
        #                 self.bot.send_document(self.last_message.chat.id, log_file)
        #             except Exception as ex:
        #                 # message.text = self.connector_func(message, ex)
        #                 # print(ex)
        #                 pass

        #         else:
        #             print(start_data)
        #             time.sleep(random.randrange(169, 179))
        #         # //////////////////////////////////////////////////////////////////////////////////////
        #         if not delay_true and self.calibrator_flag and 15 <= self.left_time_in_minutes_func(self.listing_time_ms) <= 20:
        #             self.delay_manager()
        #             delay_true = True
        #         if 0 < self.left_time_in_minutes_func(self.listing_time_ms) <= 10:
        #             self.trading_little_temp(set_item) # main func
        #             # //////////////////////////////////////////////////////////////////////////// 
        #             delay_true = False
        #             try:
        #                 result_time, self.response_data_list = self.show_trade_time(self.response_data_list, 'bitget')                        
        #                 self.last_message.text = self.connector_func(self.last_message, result_time)
        #                 print(result_time)  
        #                 cur_time = int(time.time()* 1000)
        #                 total_log_instance.json_to_buffer('PARS', cur_time, start_data)                        
        #                 cur_time = int(time.time()* 1000)
        #                 total_log_instance.json_to_buffer('START', cur_time, set_item_for_write)  
        #                 cur_time = int(time.time()* 1000)
        #                 total_log_instance.json_to_buffer('TRADES', cur_time, self.response_data_list)   
        #                 json_file = total_log_instance.get_json_data()                
        #                 self.bot.send_document(self.last_message.chat.id, json_file)   
        #                 log_file = total_log_instance.get_logs()
        #                 self.bot.send_document(self.last_message.chat.id, log_file)       
        #             except Exception as ex:
        #                 # message.text = self.connector_func(message, ex)
        #                 # print(ex)
        #                 pass
        #             time.sleep(30)
        #             continue

        #         self.last_message.text = self.connector_func(self.last_message, "pause...")
        #         # print("pause...")
        #         time.sleep(random.randrange(169, 179)) 
        # # ////////////////////////////////////////////////////////////   
        # # print(self.SOLI_DEO_GLORIA)
        # self.last_message.text = self.connector_func(self.last_message, self.SOLI_DEO_GLORIA)


    
    # @log_exceptions_decorator
    # def from_string_to_date_time(self, date_time_str):
    #     pattern = r'(\d{1,2})(?:st|nd|rd|th) (\w+) (\d{4}), (\d{1,2}):(\d{2}) \(UTC\)'
    #     match = re.match(pattern, date_time_str)
    #     if match:            
    #         day = int(match.group(1))
    #         month_str = match.group(2)
    #         year = int(match.group(3))
    #         hour = int(match.group(4))
    #         minute = int(match.group(5))
    #         months = {
    #             'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
    #             'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
    #         }
    #         month = months.get(month_str)
    #         if month:
    #             dt = dttm(year, month, day, hour, minute)
    #             milliseconds = int(dt.timestamp() * 1000)
    #             return milliseconds
    #     return

    # def symbol_extracter(self, text):    
    #     matches = re.findall(r'\((.*?)\)', text)
    #     extracted_text = [re.sub(r'[\(\)\.,\-!]', '', match) for match in matches]
    #     return extracted_text 

# pipreqs /путь_к_вашему_проекту --force --ignore .venv
