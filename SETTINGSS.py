is_only_terminale = True # только терминал/только терминал + тг интерфейс
is_switch_on = True # бот включен/бот отключен

class PARAMS():
    def __init__(self) -> None:
        self.railway_server_number = 1 # номер сервера
        self.work_to = 17 # hoor in UTC до скольки работать
        self.sleep_to = 5 # hoor in UTC до скольки спать
        self.price_threshold = 2.0 # минимальный множитель цены -- биды к аскам