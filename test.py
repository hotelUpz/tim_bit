# import time
# def milliseconds_to_datetime(milliseconds):
#     import datetime
#     # time_correction = 10800000
#     # milliseconds = milliseconds
#     seconds, milliseconds = divmod(milliseconds, 1000)
#     time = datetime.datetime.utcfromtimestamp(seconds)
#     milliseconds_str = str(milliseconds).zfill(3)
#     return time.strftime('%Y-%m-%d %H:%M:%S') + '.' + milliseconds_str

# t = int(time.time()*1000)
# print(milliseconds_to_datetime(t))
# 1711605532000

# import time

# def next_two_minutes_ms():
#     return ((int(time.time() * 1000) + 120000) // 60000) * 60000

# next_2_minute_ms = next_two_minutes_ms()
# print(milliseconds_to_datetime(next_2_minute_ms))

# # Рассчитываем задержку до следующей минуты
# delay_ms = next_minute_ms - current_time_ms

# # Переводим задержку в секунды и спим
# time.sleep(delay_ms / 1000)



# import time
# print(1711203599845 - time.time()*1000)

# test_symbol_list = ['ARBUSDT', 'BGBUSDT']
# print(test_symbol_list[:1])

# import time
# import random
# from info_parser import ANNONCEMENT

# class YourClass:
#     def __init__(self):
#         self.controls_mode = 'a'
#         self.calibrator_flag = True
#         self.delay_time_ms = 0
#         self.default_params = {}

#     def main(self): 
#         while True:


#             # Получаем информацию о начале работы
#             if self.controls_mode == 'a':  
#                 start_data = ANNONCEMENT().bitget_parser()             
#                 set_item, listing_time_ms = self.params_gather(start_data, self.market_place, self.controls_mode, self.delay_time_ms, self.default_params)

#                 # Рассчитываем оставшееся время до начала работы
#                 time_left_minutes = round((set_item['listing_time_ms'] - current_time_ms) / (1000 * 60), 2)
#                 print(f"{time_left_minutes} min is left...")

#                 # Если установлен флаг калибровки и время до начала работы находится в диапазоне от 15 до 20 минут, запускаем калибратор
#                 if self.calibrator_flag and 15 <= time_left_minutes <= 20:
#                     self.delay_manager()

#                 # Если время до начала работы находится в диапазоне от 10 до 0 минут, выполняем работу
#                 if 0 < time_left_minutes <= 10:
#                     self.trading_little_temp(set_item)

#                 print("while sleep...")
#                 time.sleep(random.randrange(169, 179)) 

#     def datetime_to_milliseconds(self, datetime_str):           
#         dt_obj = time.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
#         return int(time.mktime(dt_obj) * 1000)

# from itertools import combinations

# # Ваш массив вложенных списков
# array_p = [['a'], ['b'], ['c'], ['d']]

# # Генерация всех комбинаций по 2 из элементов массива
# all_combinations = list(combinations(array_p, 2))

# # Преобразование кортежей в списки
# result_list = [[pair[0], pair[1]] for pair in all_combinations]
# print(all_combinations)
# print(result_list)

# # Вывод результатов
# for combination in all_combinations:
#     print(f"{combination[0]} - {combination[1]}")


# import re

# input_string = "123def456ghi789"
# # result = re.match(r'\d+', input_string).group()

# print(re.match(r'\d+', input_string).group())  # Выводит "123"
# x = 'dlgjhfjvn'
# new_x = x.replace('.', '')
# print(new_x)
# a = 'DkfBvh'
# print(a.capitalize())
# date_time_str = ' 2nd      April  2024,  11:00         (UTC) '
# # matches = [x.strip() for x in date_time_str.strip().split(' ') if x and x != ' ']
# matches = [x for x in date_time_str.strip().split(' ') if x.strip()]

# print(matches)
# x = ' '
# print(x.strip())


# import functools
# from utils import log_exceptions_decorator
# # Example of usage:
# @log_exceptions_decorator
# def example_function(x, y):
#     return int('dkfgh')

# # When calling the decorated function, any exceptions will be logged
# result = example_function(10, 0)
timedelta_stamps_value = 1
timedelta_stamps = {
    "days": "days",
    "hours": "hours",
    "minutes": "minutes",
    "seconds": "seconds"
}

print(list(timedelta_stamps.keys()))