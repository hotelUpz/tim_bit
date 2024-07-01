is_only_terminale = True # только терминал/только терминал + тг интерфейс
is_switch_on = False # бот включен/бот отключен

class PARAMS():
    def __init__(self) -> None:
        self.common_depo = 20 # депозит в usdt
        self.is_proxies_true = True # использовать/не использовать прокси
        self.calibrator_flag = False # флаг калибровки. Высчитывает оптимальную задержку
        self.common_delay_time_ms = 90 # задержка времени перед отправкой запроса на покупку. Общее для всех веток    
        self.work_to = 23 # hoor in UTC работать до
        self.sleep_to = 5 # hoor in UTC спать до
        self.symbol_list_el_position = 0 # если спарсен список монет, то номер монеты в списке