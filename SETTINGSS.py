is_only_terminale = False # только терминал/только терминал + тг интерфейс
is_switch_on = True # бот включен/бот отключен

class PARAMS():
    def __init__(self) -> None:
        self.railway_server_number = 1 # номер сервера
        self.work_to = 23 # hoor in UTC до скольки работать
        self.sleep_to = 4 # hoor in UTC до скольки спать
        self.price_threshold = 1.1 # минимальный множитель цены -- биды к аскам
        self.is_order_book_defencive_meh = True