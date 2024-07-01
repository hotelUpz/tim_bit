from SETTINGSS import is_only_terminale
from tg_interface import TG_MANAGER

if __name__=="__main__": 
    if is_only_terminale:
        TG_MANAGER().main_func() 
    else:
        print('Please go to the Telegram bot interface!')     
        bot = TG_MANAGER()   
        bot.run()