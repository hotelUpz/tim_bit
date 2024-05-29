# from api_bitget import BITGET_API

# class TEST(BITGET_API):

#     def __init__(self) -> None:
#         super().__init__()
#         self.response_data_list = []
#         self.response_success_list = []

#     def buy_market_temp(self, symbol, depo):  
#         response = self.place_market_order(symbol, 'BUY', depo)                
#         response = response.json() 
#         response['symbol'] = symbol
#         response['side'] = 'BUY'
#         response['status'] = 'filled'                           
#         self.response_data_list.append(response)                   
#         if response['msg'] == 'success': 
#             print('buy success!')
#             self.response_success_list.append(response)

#     def sell_market_temp(self, item):      
#         response = None               
#         response = self.place_market_order(item['data'][0]['symbol'], 'SELL', item['qnt_to_sell_start'])           
#         response = response.json()
#         response['symbol'] = item['data'][0]['symbol']
#         response['side'] = 'SELL' 
#         response['status'] = 'filled' 
#         self.response_data_list.append(response)   
#         if response['msg'] == 'success':
#             print('sell success!')  
#         else:                
#             print(f"Symbol: {item['data'][0]['symbol']}:... some problems with placing the sell order")
        
#     def extract_data_temp(self, item): 
#         response_data = []           
#         orderId = item['data']['orderId']            
#         response_data = self.get_order_data(orderId).json()
#         # print(response_data)
#         response_data['done'] = False
#         response_data['qnt_to_sell_start'] = 0
#         response_data['real_price'] = 0
        
#         try:
#             fills = response_data.get("data", [])
            
#             base_volume = sum(float(fill.get("baseVolume", 0)) for fill in fills)
#             # quote_volume = sum(float(fill.get("quoteVolume", 0)) for fill in fills)
            
#             if base_volume >= 10:
#                 response_data['qnt_to_sell_start'] = int(base_volume * 0.98)
#             elif 1 < base_volume < 10:
#                 response_data['qnt_to_sell_start'] = int(base_volume)
#             else:
#                 response_data['qnt_to_sell_start'] = round(base_volume * 0.98, 4)
            
#             if response_data['qnt_to_sell_start'] != 0:
#                 print(response_data['qnt_to_sell_start'])
#                 print(type(response_data['qnt_to_sell_start']))
#                 response_data['done'] = True
#                 item_copy = item.copy()
#                 item_copy.update(response_data)
#                 self.response_data_list.append(item_copy) 
#                 # return response_data_list_glob
#         except Exception as ex:
#             print(ex)

#     def sell_manager(self, time_arg = 1.6):
#         import time
#         time.sleep(time_arg/2)
#         for i in range(1, 3, 1):
#             try:
#                 self.extract_data_temp(self.response_success_list[2-i])
#             except Exception as ex:
#                 print(ex)     
#             # ///////////////////////////////////////////////////////                         
#             if all(not item.get('done', False) for item in self.response_data_list):
#                 print(f"Some problems with fetching trades data. Attempts number {i}")
#                 continue
#             else:
#                 for item in self.response_data_list:
#                     if item.get('done'):                        
#                         time_pause = time_arg/2 if i == 1 else 0
#                         time.sleep(time_pause)
#                         self.sell_market_temp(item)
#                         break
#                 return

#     def go_test(self, symbol, depo):                                
#         self.buy_market_temp(symbol, depo)
#         if len(self.response_success_list) != 0:
#             self.sell_manager()        
#         else:
#             print('Some problems with placing buy market orders...')  

# TEST().go_test('ARBUSDT', 10)





            # if response_data['qnt_to_sell_start'] != 0:
            #     response_data['done'] = True
            #     item_copy = item.copy()
            #     item_copy.update(response_data)                
            #     # formatted_qnt_to_sell_start = format(decimal.Decimal(response_data['qnt_to_sell_start']), '.8f')
            #     # real_buy_price = decimal.Decimal(quote_volume) / decimal.Decimal(base_volume) if base_volume != 0 else 0
            #     # real_buy_price = format(real_buy_price, '.8f')                
            #     self.response_data_list.append(item_copy) 
            #     # self.message_template(f"qnt_to_sell_start {item_copy['symbol']}: {formatted_qnt_to_sell_start}\n\n"f"buy_price {item_copy['symbol']}: {real_buy_price}")

# # /// первый код
# import requests
# import numpy as np

# def get_order_book(symbol, limit=10):
#     url = f"https://api.bitget.com/api/v2/spot/market/orderbook?symbol={symbol}&type=step0&limit={limit}"
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         data = response.json()
#         asks = data['data']['asks']
#         bids = data['data']['bids']
#         return asks[-4:], bids[-4:]
#     else:
#         print(f"Error: {response.status_code}, {response.text}")
#         return None
# symbol = 'BCPUSDT'
# order_book_data = get_order_book(symbol)
# if order_book_data:
#     # print(order_book_data[0])
#     midle_ask_price = sum(float(x[0]) for x in order_book_data[0] if x)/ 4
#     midle_bid_price = sum(float(x[0]) for x in order_book_data[1] if x)/ 4
#     print(midle_ask_price)
#     print(midle_bid_price)

# # /// первый код
# import requests
# import numpy as np

# def get_order_book(symbol, limit=5):
#     url = f"https://api.bitget.com/api/v2/spot/market/orderbook?symbol={symbol}&type=step0&limit={limit}"
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         data = response.json()
#         asks = data['data']['asks']
#         bids = data['data']['bids']
#         return asks[-4:], bids[-4:]
#     else:
#         print(f"Error: {response.status_code}, {response.text}")
#         return None
# symbol = 'BCPUSDT'
# order_book_data = get_order_book(symbol)
# if order_book_data:
#     # print(order_book_data[0])
#     midle_ask_price = sum(float(x[0]) for x in order_book_data[0] if x)/ 4
#     midle_bid_price = sum(float(x[0]) for x in order_book_data[1] if x)/ 4
#     print(midle_ask_price)
#     print(midle_bid_price)

# # /// второй код
# import requests
# # import numpy as np
# import time

# def test():
#     def get_order_book(symbol, limit=10):
#         url = f"https://api.bitget.com/api/v2/spot/market/orderbook?symbol={symbol}&type=step0&limit={limit}"
#         response = requests.get(url)
        
#         if response.status_code == 200:
#             data = response.json()
#             asks = data['data']['asks']
#             bids = data['data']['bids']
#             return asks, bids
#         else:
#             print(f"Error: {response.status_code}, {response.text}")
#             return None
        
#     def is_book_price_belov_price_threshold(asks, bids, price_threshold):
#         asks_and_bids = []

#         for ask, bid in zip(asks[:5], bids[:5]):
#             if isinstance(ask, (list, tuple)) and len(ask) > 0:
#                 try:
#                     ask_price = float(ask[0])
#                     if ask_price != 0:
#                         asks_and_bids.append(ask_price)
                        
#                 except:
#                     pass
#             if isinstance(bid, (list, tuple)) and len(bid) > 0:
#                 try:
#                     bid_price = float(bid[0])
#                     if bid_price != 0:
#                         asks_and_bids.append(bid_price)
#                 except:
#                     pass

#         if (sum(asks_and_bids) != 0) and (len(asks_and_bids) != 0):                                                   
#             last_bid_ask_price_sum = sum(asks_and_bids) / (len(asks_and_bids))
#             if last_bid_ask_price_sum < price_threshold:
#                 # print(f"last_bid/ask_price: {last_bid_ask_price_sum}")
#                 return True            
#         return False


#     symbol = 'BEERUSDT'
#     order_book_data = get_order_book(symbol, limit=10)

#     if order_book_data:
#         asks, bids = order_book_data 
#         # print(asks)
#         is_moving_on_true = is_book_price_belov_price_threshold(asks, bids, 2.0)
#         print(f"is_moving_on_true: {is_moving_on_true}")

# start_time = int(time.time()*1000)
# test()
# fin_time = int(time.time()*1000)
# delta_timee = fin_time - start_time
# print(f"delta_timee: {delta_timee}")




#     # def is_book_price_belov_price_threshold(self, asks, bids, price_threshold):
#     #     ask_prices = []
#     #     bid_prices = []

#     #     for ask, bid in zip(asks[:5], bids[:5]):
#     #         if isinstance(ask, (list, tuple)) and len(ask) > 0:
#     #             try:
#     #                 ask_price = float(ask[0])
#     #                 if ask_price != 0:
#     #                     ask_prices.append(ask_price)
                        
#     #             except:
#     #                 pass
#     #         if isinstance(bid, (list, tuple)) and len(bid) > 0:
#     #             try:
#     #                 bid_price = float(bid[0])
#     #                 if bid_price != 0:
#     #                     bid_prices.append(bid_price)
#     #             except:
#     #                 pass
#     #     asks_and_bids = ask_prices + bid_prices
#     #     if (sum(asks_and_bids) != 0) and (len(ask_prices)+len(bid_prices) != 0):                                                   
#     #         last_bid_ask_pricesum = sum(asks_and_bids) / (len(ask_prices)+len(bid_prices))
#     #         if last_bid_ask_pricesum < price_threshold:
#     #             print(f"last_bid/ask_price: {last_bid_ask_pricesum}")
#     #             return True            
#     #     return False


# # def is_book_price_below_price_threshold(asks, bids, price_threshold):
# #     try:
# #         # Объединяем аски и биды в один список
# #         prices = [float(order[0]) for order in asks[:5] + bids[:5] if isinstance(order, (list, tuple)) and len(order) > 0 and float(order[0]) != 0]
        
# #         # Если список пустой, возвращаем False
# #         if not prices:
# #             return False
        
# #         # Вычисляем среднее значение цен
# #         avg_price = sum(prices) / len(prices)
        
# #         # Проверяем, находится ли среднее значение ниже порогового
# #         if avg_price < price_threshold:
# #             print(f"Средняя цена: {avg_price}")
# #             return True
# #         else:
# #             return False
# #     except Exception as e:
# #         print(f"Произошла ошибка: {e}")
# #         return False

