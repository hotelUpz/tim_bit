from SETTINGSS import is_only_terminale, is_switch_on
from tg_interface import TG_MANAGER

if __name__=="__main__": 
    if is_switch_on:        
        if is_only_terminale:
            TG_MANAGER().main_func() 
        else:
            print('Please go to the Telegram bot interface!')     
            bot = TG_MANAGER()   
            bot.run()
    else:
        print("Бот отключен")


