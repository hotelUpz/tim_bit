# import inspect
# import json
# import sys
# from datetime import datetime, timedelta
# from io import BytesIO

# class Logger():
#     def __init__(self) -> None:
#         self.logs_buffer = []
#         self.all_errors = {}
        
#     def log_to_buffer(self, file_name, line_number, exception_message):
#         self.logs_buffer.append((file_name, line_number, exception_message))

#     def log_all_errors(self, file_name, timestamp, exception_message):
#         if file_name in self.all_errors:
#             if exception_message not in self.all_errors[file_name]:
#                 self.all_errors[file_name].append((timestamp, exception_message))
#         else:
#             self.all_errors[file_name] = [(timestamp, exception_message)]

#     def get_logs(self):
#         # print(f"logs list 23str: {self.logs_buffer}")
#         file = BytesIO()
#         file.write(str(self.logs_buffer).encode('utf-8'))
#         file.name = "logs.txt"
#         file.seek(0)
#         self.logs_buffer = []
#         return file

# class JsonLogger(Logger):
#     def __init__(self):
#         super().__init__()
#         self.json_logs_buffer = []

#     def json_to_buffer(self, target, cur_time, data):
#         self.json_logs_buffer.append((target, cur_time, data))

#     def get_json_data(self):
#         # print(self.json_logs_buffer)
#         file = BytesIO()
#         file.write(json.dumps(self.json_logs_buffer, indent=4).encode('utf-8'))
#         file.name = "data.json"
#         file.seek(0)
#         self.json_logs_buffer = []
#         return file

# class Total_Logger(JsonLogger):
#     def __init__(self):
#         super().__init__()

# total_log_instance = Total_Logger()

# # def log_exceptions_decorator(func):
# #     def wrapper(*args, **kwargs):
# #         try:
# #             return func(*args, **kwargs)
# #         except Exception as ex:
# #             timestamp = datetime.utcnow()
# #             frame = sys._getframe(1)
# #             file_name = frame.f_code.co_filename
# #             line_number = frame.f_lineno
# #             exception_message = str(ex)
# #             error_info = (file_name, line_number, exception_message)
# #             total_log_instance.log_to_buffer(*error_info)
# #             total_log_instance.log_all_errors(file_name, timestamp, exception_message)
# #             print(f"Error occurred in file '{file_name}', line {line_number}: {exception_message}")
# #     return wrapper

# def log_exceptions_decorator(func):
#     def wrapper(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except Exception as ex:
#             timestamp = datetime.utcnow()
#             current_frame = inspect.currentframe()
#             caller_frame = current_frame.f_back
#             file_name = caller_frame.f_code.co_filename
#             line_number = caller_frame.f_lineno
#             exception_message = str(ex)
#             error_info = (file_name, line_number, exception_message)
#             total_log_instance.log_to_buffer(*error_info)
#             total_log_instance.log_all_errors(file_name, timestamp, exception_message)
#             print(f"Error occurred in file '{file_name}', line {line_number}: {exception_message}")
#     return wrapper


            # 'host': 'localhost',
            # 'host': 'roundhouse.proxy.rlwy.net',
            # 'port': '15775',

# # import requests
# # from bs4 import BeautifulSoup
# # get_location_link = 'https://2ip.ru'

# # proxy_host = '77.47.244.201'
# # proxy_port = '50100'
# # proxy_username = 'nikolassmsttt'
# # proxy_password = 'pRcwSxcJtT'

# # proxy_url = f'http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}'
# # proxiess = {
# #     'http': proxy_url,
# #     'https': proxy_url
# # }

# # proxy_arg = f'nikolassmsttt:pRcwSxcJtT@77.47.244.201:50100'
# # # print(proxy_url)
# # proxiess = {
# #     "https": f"http://{proxy_arg}"
# #     # 'http': proxy_url,
# #     # 'https': proxy_url
# # }

# # # Пример запроса через прокси
# # try:
# #     response = requests.get('http://example.com', proxies=proxiess)
# #     print(response.text)
# # except requests.exceptions.ProxyError as e:
# #     print(f"Proxy error: {e}")
# # except requests.exceptions.RequestException as e:
# #     print(f"Request error: {e}")

# # try:
# #     response = requests.get(url=get_location_link, proxies=proxiess)
# #     soup = BeautifulSoup(response.text, 'lxml')
# #     ip = soup.find('div', class_ = 'ip').text.strip()
# #     location = soup.find('div', class_ = 'value-country').text.strip()
# #     print(ip, ':', location)

# # except Exception as ex:
# #     print(ex)



# [{'annId': '12560603809830', 'annTitle': 'Bitget Will List VeChain (VET). Come and grab a share of $37,750 worth of VET!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809830', 'cTime': '1716202820000'}, {'annId': '12560603810139', 'annTitle': 'Bitget Will List DOG (DOG) in the Innovation and BTC Ecosystem Zone!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810139', 'cTime': '1716458429000'}, {'annId': '12560603810143', 'annTitle': 'Notice on New Trading Pairs on Bitget Spot - 24 May 2024', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810143', 'cTime': '1716465621000'}, {'annId': '12560603810104', 'annTitle': 'Bitget pre-market trading: zkLink (ZKL) is set to launch soon', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810104', 'cTime': '1716447634000'}, {'annId': '12560603809829', 'annTitle': 'Bitget Will List First Digital USD (FDUSD). Come and grab a share of $80,000 worth of FDUSD!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809829', 'cTime': '1716462007000'}, {'annId': '12560603810140', 'annTitle': 'Bitget Will List SolarX (SXCH). Come and grab a share of $129,500 Worth SXCH!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810140', 'cTime': '1716465608000'}, {'annId': '12560603810148', 'annTitle': '[Initial Listing] Bitget Will List Hiveswap (HIVP)', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810148', 'cTime': '1716469230000'}, {'annId': '12560603809549', 'annTitle': 'Bitget Will List GameStop (GME) in the Innovation, Solana and MEME Zone!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809549', 'cTime': '1715670053000'}, {'annId': '12560603810142', 'annTitle': 'Announcement on adjustment of position tier for BIGTIMEUSDT futures trading pair', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810142', 'cTime': '1716458432000'}, {'annId': '12560603810107', 'annTitle': 'Bitget pre-market trading:Lista (LISTA) is set to launch soon', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810107', 'cTime': '1716447613000'}, {'annId': '12560603809959', 'annTitle': '[Initial Listing] Bitget Will List Holograph (HLG). Come and grab a share of $89,000 worth of HLG!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809959', 'cTime': '1716292842000'}, {'annId': '12560603810064', 'annTitle': 'BICOUSDT is Now Available on Futures', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810064', 'cTime': '1716451250000'}, {'annId': '12560603810063', 'annTitle': 'HIFIUSDT is Now Available on Futures', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810063', 'cTime': '1716451256000'}, {'annId': '12560603810106', 'annTitle': 'Bitget pre-market trading: Taiko (TKO) is set to launch soon', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810106', 'cTime': '1716447631000'}, {'annId': '12560603810057', 'annTitle': 'Bitget PoolX is listing HashPack (PACK) : Stake USDT to mine PACK.', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810057', 'cTime': '1716385974000'}, {'annId': '12560603810056', 'annTitle': 'Bitget PoolX is listing SaucerSwap (SAUCE): Stake BTC to mine SAUCE.', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810056', 'cTime': '1716385691000'}, {'annId': '12560603809987', 'annTitle': 'Bitget pre-market trading: zkSync (ZKSYNC) is set to launch soon', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809987', 'cTime': '1716361215000'}, {'annId': '12560603809998', 'annTitle': 'Bitget Crypto Loan Carnival: Borrow USDT, BTC, and ETH to enjoy an ultra-low interest rate of 1.2%', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809998', 'cTime': '1716375611000'}, {'annId': '12560603810021', 'annTitle': '[Initial Listing] Bitget Will List MetaPhone (PHONE)', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810021', 'cTime': '1716375612000'}, {'annId': '12560603809977', 'annTitle': 'Exclusive ETH saving campaign for African Users : 20% APR!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809977', 'cTime': '1716363926000'}, {'annId': '12560603809902', 'annTitle': 'Bitget Will List SaucerSwap (SAUCE). Come and grab a share of 998,000 SAUCE!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809902', 'cTime': '1716292819000'}, {'annId': '12560603809901', 'annTitle': '[Initial Listing] Bitget Will List HashPack (PACK). Come and grab a share of 7,083,000 PACK!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809901', 'cTime': '1716292856000'}, {'annId': '12560603809810', 'annTitle': '[Initial Listing] Bitget Will List NYAN (NYAN)', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809810', 'cTime': '1716184842000'}, {'annId': '12560603809831', 'annTitle': '[Initial Listing] Bitget Will List Thetanuts Finance (NUTS). Come and grab a share of 1,266,666 NUTS!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809831', 'cTime': '1716195621000'}, {'annId': '12560603809836', 'annTitle': 'Bitget PoolX is listing Thetanuts Finance (NUTS) : Stake BGB to mine NUTS', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809836', 'cTime': '1716188400000'}, {'annId': '12560603809821', 'annTitle': 'Bitget pre-market trading:Layerzero(ZRO) is set to launch soon', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809821', 'cTime': '1716177648000'}, {'annId': '12560603809824', 'annTitle': 'Bitget to support 3 new futures copy trading pairs', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809824', 'cTime': '1715932828000'}, {'annId': '12560603809682', 'annTitle': 'Bitget Will List CATAMOTO (CATA). Come and grab a share of $50,000 worth of CATA!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809682', 'cTime': '1715857200000'}, {'annId': '12560603809811', 'annTitle': 'Announcement of Bitget spot bot on adding HODL/USDT', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809811', 'cTime': '1715943521000'}, {'annId': '12560603809724', 'annTitle': 'Bitget announcement on adding support for NOT futures trading, spot margin trading, copy trading, and trading bots', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809724', 'cTime': '1715863816000'}, {'annId': '12560603809762', 'annTitle': 'Announcement on adjustment of position tiers for multiple USDT-M perpetual futures trading pairs', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809762', 'cTime': '1715931057000'}, {'annId': '12560603809764', 'annTitle': 'Bitget PoolX is listing HODL (HODL) : Stake ETH to mine HODL', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809764', 'cTime': '1715929200000'}, {'annId': '12560603809763', 'annTitle': 'Bitget PoolX is listing Daoversal (DAOT): Stake BTC to mine DAOT', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809763', 'cTime': '1715929200000'}, {'annId': '12560603809725', 'annTitle': 'Bitget Will List HODL (HODL)', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809725', 'cTime': '1715864413000'}, {'annId': '12560603809727', 'annTitle': 'Bitget pre-market trading: Notcoin (NOT) Delivery Will Be Delayed', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809727', 'cTime': '1715864452000'}, {'annId': '12560603809718', 'annTitle': 'Notice on Trading Postponement for DAOT/USDT', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809718', 'cTime': '1715856383000'}, {'annId': '12560603809669', 'annTitle': 'Bitget Will List Lifeform (LIFEFORM) in the Web3 and Metaverse Zone！', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809669', 'cTime': '1715842838000'}, {'annId': '12560603809636', 'annTitle': '[Initial Listing] Bitget Will List Drift protocol (DRIFT)', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809636', 'cTime': '1715763612000'}, {'annId': '12560603809657', 'annTitle': 'Exclusive opportunity: join the Bitget TG signal bot beta test now! ', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809657', 'cTime': '1715839211000'}, {'annId': '12560603809668', 'annTitle': '[Initial Listing] Bitget Will List Daoversal (DAOT)', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809668', 'cTime': '1715824854000'}, {'annId': '12560603809464', 'annTitle': ' [Initial Listing] Bitget Will List Wisdomise AI (WSDM). Come and grab a share of $41,000 Worth of WSDM!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809464', 'cTime': '1715598016000'}, {'annId': '12560603809476', 'annTitle': 'Bitget Will List BounceBit (BB). Come and grab a share of $40,000 Worth of BB!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809476', 'cTime': '1715587229000'}, {'annId': '12560603809597', 'annTitle': '[Initial Listing] Bitget Will List Notcoin (NOT). Come and grab a share of $40,000 worth of NOT!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809597', 'cTime': '1715752848000'}, {'annId': '12560603809632', 'annTitle': 'Bitget Crypto Loan Carnival: Borrow USDT, BTC, and ETH to enjoy an ultra-low interest rate of 1.2%', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809632', 'cTime': '1715770808000'}, {'annId': '12560603809633', 'annTitle': 'Bitget PoolX is listing Wisdomise AI (WSDM) : Stake USDT to mine WSDM', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809633', 'cTime': '1715756400000'}, {'annId': '12560603809596', 'annTitle': '[Initial Listing] Bitget Will List Engines of Fury (FURY). ', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809596', 'cTime': '1715684445000'}, {'annId': '12560603809551', 'annTitle': 'Bitget Will List Canxium (CAU). Come and grab a share of 3,430 CAU!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809551', 'cTime': '1715684402000'}, {'annId': '12560603809577', 'annTitle': 'Bitget Will List Virtual Protocol (VIRTUAL). Come and grab a share of $24,000 worth of VIRTUAL!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809577', 'cTime': '1715691620000'}, {'annId': '12560603809477', 'annTitle': 'Bitget Will List FUD (FUD). Come and grab a share of 151,415,000,000 FUD!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809477', 'cTime': '1715598054000'}, {'annId': '12560603809537', 'annTitle': 'Bitget announcement on adding support for BB futures trading, spot margin trading, copy trading, and trading bots', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809537', 'cTime': '1715598497000'}, {'annId': '12560603809497', 'annTitle': 'Bitget PoolX is listing Alltoscan (ATS) : Stake BGB to mine ATS', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809497', 'cTime': '1715583600000'}, {'annId': '12560603809532', 'annTitle': 'Bitget Futures Bot adds VGXUSDT', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809532', 'cTime': '1715593457000'}, {'annId': '12560603809529', 'annTitle': 'VGXUSDT is Now Available on Futures', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809529', 'cTime': '1715590336000'}, {'annId': '12560603809443', 'annTitle': 'Bitget Will List iMe Lab (LIME). Come and grab a share of 364,000 LIME!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809443', 'cTime': '1715346044000'}, {'annId': '12560603809462', 'annTitle': 'New spot margin trading pair — TONCOIN/USDT!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809462', 'cTime': '1715570473000'}, {'annId': '12560603809419', 'annTitle': '[Initial Listing] Bitget Will List Bubble (BUBBLE). Come and grab a share of 10,999,999 BUBBLE!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809419', 'cTime': '1715338808000'}, {'annId': '12560603808928', 'annTitle': 'Bitget Futures Bot adds LSKUSDT', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603808928', 'cTime': '1714369263000'}, {'annId': '12560603809406', 'annTitle': 'Bitget pre-market trading: Notcoin (NOT) is set to launch soon', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809406', 'cTime': '1715324400000'}, {'annId': '12560603809445', 'annTitle': 'Bitget to support 5 new spot copy trading pairs', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809445', 'cTime': '1715337567000'}, {'annId': '12560603808541', 'annTitle': '[Initial Listing] Bitget Will List Gptverse  (GPTV). Come and grab a share of 5,333,333 GPTV!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603808541', 'cTime': '1714384801000'}, {'annId': '12560603809415', 'annTitle': 'Bitget pre-market trading: io.net (IO) is set to launch soon', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809415', 'cTime': '1715328000000'}, {'annId': '12560603809395', 'annTitle': 'Notice on New Trading Pairs on Bitget Spot - 10 May 2024', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809395', 'cTime': '1715250655000'}, {'annId': '12560603809411', 'annTitle': 'ADAUSD is Now Available on Futures', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809411', 'cTime': '1715328057000'}, {'annId': '12560603809282', 'annTitle': 'Bitget Will List Alltoscan (ATS). Come and grab a share of 26,100 ATS!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809282', 'cTime': '1715338813000'}, {'annId': '12560603809107', 'annTitle': '[Initial Listing] Bitget Will List ZeroLend (ZEROLEND) in the Innovation and DeFi Zone. ', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809107', 'cTime': '1714809633000'}, {'annId': '12560603808919', 'annTitle': '[Initial Listing] Bitget Will List STYLE Protocol (STYLE). Come and grab a share of $96,000 worth of STYLE!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603808919', 'cTime': '1714388452000'}, {'annId': '12560603809371', 'annTitle': 'Bitget Crypto Loan adds CORE, FLOKI, WLD, ARKM and more.', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809371', 'cTime': '1715252448000'}, {'annId': '12560603809391', 'annTitle': 'Bitget Futures Bot adds XVSUSDT, MOVRUSDT', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809391', 'cTime': '1715245416000'}, {'annId': '12560603808694', 'annTitle': 'Bitget TraderPro: Invite new users and get 100 USDT!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603808694', 'cTime': '1713943171000'}, {'annId': '12560603809367', 'annTitle': 'Exclusive USDT saving campaign for African Users : 15% APR!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809367', 'cTime': '1715237910000'}, {'annId': '12560603809366', 'annTitle': 'Bitget PoolX is listing Gptverse (GPTV) : Stake BTC to mine GPTV', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809366', 'cTime': '1715232600000'}, {'annId': '12560603809365', 'annTitle': 'Bitget PoolX is listing Apeiron (APRS) : Stake ETH to mine APRS', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809365', 'cTime': '1715232600000'}, {'annId': '12560603809220', 'annTitle': 'Bitget Will List Roseon (ROSX). Come and grab a share of 2,265,000 ROSX!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809220', 'cTime': '1715166033000'}, {'annId': '12560603809290', 'annTitle': 'XVSUSDT is Now Available on Futures', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809290', 'cTime': '1715155242000'}, {'annId': '12560603809291', 'annTitle': 'MOVRUSDT is Now Available on Futures', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809291', 'cTime': '1715155226000'}, {'annId': '12560603809194', 'annTitle': 'Bitget Will List Apeiron (APRS). Come and grab a share of 410,700 APRS!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809194', 'cTime': '1715151633000'}, {'annId': '12560603809208', 'annTitle': 'New spot margin trading pair — CEL/USDT!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809208', 'cTime': '1715088437000'}, {'annId': '12560603809003', 'annTitle': 'Bitget PoolX is listing STYLE Protocol (STYLE) : Stake ETH and USDT to mine STYLE', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809003', 'cTime': '1714453200000'}, {'annId': '12560603809205', 'annTitle': 'Bitget Announcement on Delisting RBW Savings Product', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809205', 'cTime': '1715058057000'}, {'annId': '12560603809158', 'annTitle': 'Bitget Will List Mode (MODE) in the Innovation and Layer 2 Zone!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809158', 'cTime': '1715068811000'}, {'annId': '12560603808844', 'annTitle': 'Bitget Will List LandX Finance (LNDX). Come and grab a share of $78,000 Worth of LNDX!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603808844', 'cTime': '1714647601000'}, {'annId': '12560603809095', 'annTitle': 'Bitget Pre-Market Trading: ZeroLend (ZEROLEND) is set to launch soon', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809095', 'cTime': '1714543200000'}, {'annId': '12560603809091', 'annTitle': 'Bitget announcement on adding support for REZ futures trading, spot margin trading, copy trading, and trading bots', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809091', 'cTime': '1714482751000'}, {'annId': '12560603809000', 'annTitle': 'Bitget pre-market trading: EigenLayer (EIGEN) is set to launch soon', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809000', 'cTime': '1714460444000'}, {'annId': '12560603809041', 'annTitle': '[Initial Listing] Bitget Will List Kamino (KMNO)', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809041', 'cTime': '1714464000000'}, {'annId': '12560603809040', 'annTitle': 'Bitget Wealth Management concludes April with an APR of 10%', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809040', 'cTime': '1714557604000'}, {'annId': '12560603808927', 'annTitle': 'Bitget Will List Renzo (REZ). Come and grab a share of $22,000 Worth of REZ!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603808927', 'cTime': '1714388445000'}, {'annId': '12560603808994', 'annTitle': 'GLMUSDT is Now Available on Futures', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603808994', 'cTime': '1714464031000'}, {'annId': '12560603808999', 'annTitle': 'Bitget PoolX is listing UNDEADS GAMES (UDS) : Stake BGB and USDT to mine UDS', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603808999', 'cTime': '1714449600000'}, {'annId': '12560603808998', 'annTitle': 'Bitget PoolX is listing KATT DADDY (KATT) : Stake BGB and USDT to mine KATT', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603808998', 'cTime': '1714449600000'}, {'annId': '12560603808785', 'annTitle': 'Bitget pre-market trading:  Meson Network (MSN) is set to launch soon', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603808785', 'cTime': '1714035659000'}, {'annId': '12560603808843', 'annTitle': ' Bitget Will List Undeads Games (UDS). Come and grab a share of $78,000 Worth of UDS!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603808843', 'cTime': '1714388429000'}, {'annId': '12560603808915', 'annTitle': 'Bitget to support 7 new spot copy trading pairs', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603808915', 'cTime': '1714290564000'}, {'annId': '12560603808851', 'annTitle': 'Bitget Will List MANEKI Neko (MANEKI). Come and grab a share of $11,000 worth of MANEKI!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603808851', 'cTime': '1714129243000'}, {'annId': '12560603808842', 'annTitle': 'Bitget Will List Meson Network (MSN). Come and grab a share of $17,000 worth of MSN!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603808842', 'cTime': '1714129242000'}, {'annId': '12560603808816', 'annTitle': 'Bitget Will List CatGPT (CATGPT)', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603808816', 'cTime': '1714046400000'}, {'annId': '12560603808849', 'annTitle': 'Bitget Will List SIX Network (SIX). Come and grab a share of $23,000 worth of SIX!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603808849', 'cTime': '1714129241000'}, {'annId': '12560603808837', 'annTitle': 'Bitget PoolX is listing Green Bitcoin (GBTC) : Stake BTC to mine GBTC', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603808837', 'cTime': '1714098600000'}, {'annId': '12560603808787', 'annTitle': 'Bitget Will List Bitkub Coin (KUB). Come and grab a share of $23,000 worth of KUB!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603808787', 'cTime': '1714042851000'}]
     
            # notice_symbol = 'DMR'
            # and not any(x for x in symbol_data if x == notice_symbol)