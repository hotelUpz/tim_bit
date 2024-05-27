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