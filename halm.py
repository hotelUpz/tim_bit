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