# from SETTINGSS import is_only_terminale, is_switch_on
# from tg_interface import TG_MANAGER

# if __name__=="__main__": 
#     if is_switch_on:        
#         if is_only_terminale:
#             TG_MANAGER().main_func() 
#         else:
#             print('Please go to the Telegram bot interface!')     
#             bot = TG_MANAGER()   
#             bot.run()
#     else:
#         print("Бот отключен")

# import requests
# from bs4 import BeautifulSoup
# from joblib import Parallel, delayed
# import time
# import random
# from random import choice
# from utils import UTILS, time_correction

# user_agents = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
# ]

# bitget_headers = {
#     'authority': 'www.bitget.com',    
#     # 'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
#     'origin': 'https://www.bitget.com/',
#     'referer': 'https://www.bitget.com/',
#     # 'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
#     # 'sec-ch-ua-mobile': '?0',   
#     # 'sec-fetch-dest': 'script',
#     # 'sec-fetch-mode': 'cors',
#     # 'sec-fetch-site': 'cross-site',
#     'User-Agent': choice(user_agents)
# }

# class ANNONCEMENT(UTILS):
#     def __init__(self) -> None:
#         super().__init__()
#         self.session = requests.Session()

#         self.proxy_url = f'socks5://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_socks5_port}'
#         self.proxiess = {
#             # 'https': self.proxy_url,
#             'http': self.proxy_url,            
#         }
#         # print(self.proxy_url)

#         # self.proxy_url = f'http://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}'
#         # self.proxiess = {
#         #     'https': self.proxy_url,
#         #     'http': self.proxy_url,            
#         # }
#         # print(self.proxy_url)
#         # self.links_multiprocessor = self.log_exceptions_decorator(self.links_multiprocessor)
#         # self.bitget_parser = self.log_exceptions_decorator(self.bitget_parser)

#     def links_multiprocessor(self, data, cur_time, cpu_count=2): 
#         total_list = []
#         try:
#             res = Parallel(n_jobs=cpu_count, prefer="threads")(delayed(lambda item: self.bitget_links_handler(item, cur_time))(item) for item in data)
#             for x in res: 
#                 if x:               
#                     try:                    
#                         total_list += x 
#                     except:
#                         pass 
#         except:
#             pass
#         return total_list

#     def bitget_links_handler(self, data_item, cur_time):
#         data_set = []
#         try:
#             r = None
#             bitget_headers['User-Agent'] = choice(user_agents)
#             # print(bitget_headers)
#             time.sleep(random.randint(1, 5))
#             # r = self.session.get(url=data_item['annUrl'], headers=bitget_headers, proxies=self.proxiess if self.is_proxies_true else None)
#             # print(r)
#             r = self.session.get(url=data_item['annUrl'])
#             print(r)
#             if r is not None and r.status_code == 200:
#                 soup = BeautifulSoup(r.text, 'html.parser')
#                 listing_time_all_potential_string = soup.find('div', class_='ArticleDetails_actice_details_main__oIjfu').get_text()
#                 trading_time_str = [x for x in listing_time_all_potential_string.split('\n') if "Trading Available:" in x][0].replace("Trading Available:", "").strip()
#                 # print(trading_time_str)
#                 listing_time = self.from_string_to_date_time(trading_time_str) 
#                 # print(listing_time) 
#                 # symbol_data = self.symbol_extracter(data_item['annTitle'])  
#                 # print(symbol_data)  
#                 if listing_time > cur_time - (10*time_correction):
#                     # print(listing_time > cur_time - time_correction)
#                     symbol_data = self.symbol_extracter(data_item['annTitle'])  
#                     # print(symbol_data) 
#                     if symbol_data:
#                         data_set.append(
#                             {                                
#                                 "symbol_list": [x.strip() + 'USDT' for x in symbol_data if x.strip()],                                
#                                 "listing_time_ms": listing_time + time_correction, 
#                                 "listing_time": self.milliseconds_to_datetime_for_parser(listing_time + time_correction + 10800000),
#                                 "link": data_item['annUrl']             
#                             }
#                         )
#         except Exception as ex:
#             pass
#             # self.handle_messagee(ex)                    
#         return data_set
                 
#     def bitget_parser(self):
#         # print('Start parser')
#         pars_data = []
#         try:
#             r = None
#             start_time = self.get_start_of_day()
#             url = f"https://api.bitget.com/api/v2/public/annoucements?&annType=coin_listings&language=en_US"        
#             r = self.session.get(url)
#             print(r)
#             if r is not None and r.status_code == 200:
#                 r_j = r.json()
#                 data = r_j["data"]        
#                 data = [{**x, "cTime": int(float(x["cTime"]))} for x in data if int(float(x["cTime"])) > start_time]
#                 # print(data)
#                 cur_time = int(time.time()* 1000)
#                 bitget_headers['User-Agent'] = choice(user_agents)
#                 pars_data = self.links_multiprocessor(data, cur_time)
#         except Exception as ex:
#             pass
#         return pars_data

import requests
import time
from random import choice
from bs4 import BeautifulSoup

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
]

bitget_headers = {
    'authority': 'www.bitget.com',    
    'origin': 'https://www.bitget.com/',
    'referer': 'https://www.bitget.com/',
    'User-Agent': choice(user_agents)
}

def get_announcements():
    url = "https://api.bitget.com/api/v2/public/annoucements?&annType=coin_listings&language=en_US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get("data", [])
        return data
    else:
        print(f"Failed to fetch announcements. Status code: {response.status_code}")
        return []

def parse_listing_page(url):
    try:
        headers = bitget_headers
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            details = soup.find('div', class_='ArticleDetails_actice_details_main__oIjfu').get_text()
            trading_time_str = [x for x in details.split('\n') if "Trading Available:" in x][0].replace("Trading Available:", "").strip()
            return trading_time_str
        else:
            print(f"Failed to fetch listing page. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error while parsing listing page: {e}")
        return None

def main():
    announcements = get_announcements()
    for announcement in announcements:
        url = announcement.get('annUrl')
        title = announcement.get('annTitle')
        if url and title:
            print(f"Parsing {title}")
            trading_time = parse_listing_page(url)
            if trading_time:
                print(f"Trading time for {title}: {trading_time}")
            else:
                print(f"Failed to fetch trading time for {title}")
            time.sleep(2)  # Adding delay to avoid being blocked

if __name__ == "__main__":
    main()
