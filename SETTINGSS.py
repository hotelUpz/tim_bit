is_only_terminale = False # только терминал/только терминал + тг интерфейс
is_switch_on = True # бот включен/бот отключен

class PARAMS():
    def __init__(self) -> None:
        self.railway_server_number = 1 # номер сервера
        self.work_to = 17 # hoor in UTC до скольки работать
        self.sleep_to = 4 # hoor in UTC до скольки спать
        self.price_threshold = 5 # максимальная бидовая цена
        self.price_relation_threshold = 1.1 # минимальное отношение асков к бидам
        self.is_order_book_defencive_meh = True
