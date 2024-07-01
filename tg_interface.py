from main_logic import MAIN_CONTROLLER
import os, inspect
current_file = os.path.basename(__file__)

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