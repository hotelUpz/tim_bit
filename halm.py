                    # self.trading_little_temp(set_item) # main func
                    # # //////////////////////////////////////////////////////////////////////                            
                    # try:
                    #     cur_time = int(time.time()* 1000)
                    #     result_time, self.response_data_list = self.show_trade_time(self.response_data_list, 'bitget')                        
                    #     self.last_message.text = self.connector_func(self.last_message, result_time)
                    #     # print(result_time)  
                    #     cur_time = int(time.time()* 1000)
                    #     total_log_instance.json_to_buffer('PARS', cur_time, start_data)                        
                    #     cur_time = int(time.time()* 1000)
                    #     total_log_instance.json_to_buffer('START', cur_time, [set_item])  
                    #     cur_time = int(time.time()* 1000)
                    #     total_log_instance.json_to_buffer('TRADES', cur_time, self.response_data_list)   
                    #     json_file = total_log_instance.get_json_data()                
                    #     self.bot.send_document(self.last_message.chat.id, json_file)   
                    #     log_file = total_log_instance.get_logs()
                    #     self.bot.send_document(self.last_message.chat.id, log_file)       
                    # except Exception as ex:
                    #     # message.text = self.connector_func(message, ex)
                    #     print(ex)





    # def next_one_minutes_ms(self):
    #     # for one and half min round min:
    #     return ((int(time.time() * 1000) + 90000) // 60000) * 60000
    #     # for one min:
    #     # return ((int(time.time() * 1000) + 60000) // 60000) * 60000
    #     # for two min:
    #     # return ((int(time.time() * 1000) + 120000) // 60000) * 60000 

                            # else:
                            #     self.set_item[f'depo_server{i}'] = self.common_depo
                            #     self.set_item[f'delay_time_ms_server{i}'] = self.common_delay_time_ms


# import time

# def next_minute_ms():
#     return int(time.time() * 1000), ((int(time.time() * 1000) + 60000) // 60000) * 60000, ((int(time.time() * 1000) + 90000) // 30000) * 30000, ((int(time.time() * 1000) + 120000) // 60000) * 60000

# print(next_minute_ms())

# import time

# def next_one_and_half_minute_ms():
#     return ((int(time.time() * 1000) + 90000) // 60000) * 60000

# print(next_one_and_half_minute_ms())

# for i in range(1, 5, 1):
#     print(i)
# set_changes = {
#             "depo_server1": 20,
#             "delay_time_ms_server1": 95,

#         }
# mess_temp = '\n'.join(list(f"{k}: {v}" for k, v in set_changes.items()))
# print(mess_temp)
# print(type(mess_temp))
# import random
# print(random.randrange(12,22)/ 10)
# print(random.randrange(12,22)/ 10)
# print(random.randrange(12,22)/ 10)
# print(random.randrange(12,22)/ 10)