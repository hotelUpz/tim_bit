import requests
from bs4 import BeautifulSoup
from joblib import Parallel, delayed
import time
from random import choice
from utils import UTILS, log_exceptions_decorator, time_correction

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
]

bitget_headers = {
    # 'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json;charset=UTF-8',
    'language': 'en_US',
    'locale': 'en_US',
    'origin': 'https://www.bitget.com',
    'priority': 'u=1, i',
    'referer': 'https://www.bitget.com/support/articles/12560603809959',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'terminaltype': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    
}


class ANNONCEMENT(UTILS):
    def __init__(self, proxy_host, proxy_port, proxy_username, proxy_password) -> None:
        super().__init__()
        print(proxy_host, proxy_port, proxy_username, proxy_password)
        self.session = requests.Session()
        self.session.mount('https://www.bitget.com', requests.adapters.HTTPAdapter(pool_connections=12, pool_maxsize=12))
        proxy_arg = f'{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}'    
        self.proxiess = {
            "https": f"http://{proxy_arg}"
            # 'http': proxy_url,
            # 'https': proxy_url
        }
        self.is_proxies_true = 1
    
    @log_exceptions_decorator
    def links_multiprocessor(self, data, cur_time, cpu_count=10): 
        total_list = []
        res = Parallel(n_jobs=cpu_count, prefer="threads")(delayed(lambda item: self.bitget_links_handler(item, cur_time))(item) for item in data)
        for x in res: 
            if x:               
                try:                    
                    total_list += x 
                except:
                    pass 
        return total_list
    # @log_exceptions_decorator
    def bitget_links_handler(self, data_item, cur_time):
        try:
            # print('sdjkbv')
            data_set = []
            # bitget_headers['User-Agent'] = choice(user_agents)
            r = requests.get(url=data_item['annUrl'], headers=bitget_headers, proxies=self.proxiess if self.is_proxies_true else None)
            print(r)
            # print(r.text)
            soup = BeautifulSoup(r.text, 'html.parser')
            listing_time_all_potential_string = soup.find('div', class_='ArticleDetails_actice_details_main__oIjfu').get_text()
            trading_time_str = [x for x in listing_time_all_potential_string.split('\n') if "Trading Available:" in x][0].replace("Trading Available:", "").strip()
            # print(trading_time_str)
            listing_time = self.from_string_to_date_time(trading_time_str) 
            # print(listing_time) 
            symbol_data = self.symbol_extracter(data_item['annTitle'])  
            # print(symbol_data)  
            if listing_time > cur_time - time_correction:
                # print(listing_time > cur_time - time_correction)
                symbol_data = self.symbol_extracter(data_item['annTitle'])  
                # print(symbol_data)   
                if symbol_data:
                    data_set.append(
                        {                                
                            "symbol_list": [x.strip() + 'USDT' for x in symbol_data if x.strip()],                                
                            "listing_time_ms": listing_time + time_correction, 
                            "listing_time": self.milliseconds_to_datetime_for_parser(listing_time + time_correction + 10800000),
                            "link": data_item['annUrl']             
                        }
                    )
        except:
            pass                      
        return data_set
        
    @log_exceptions_decorator                   
    def bitget_parser(self):
        # print('Start parser')
        start_time = self.get_start_of_day()
        url = f"https://api.bitget.com/api/v2/public/annoucements?&annType=coin_listings&language=en_US"        
        r = requests.get(url)
        print(r)
        r_j = r.json()
        data = r_j["data"]        
        data = [{**x, "cTime": int(float(x["cTime"]))} for x in data if int(float(x["cTime"])) > start_time]
        # print(data)
        cur_time = int(time.time()* 1000)
        return self.links_multiprocessor(data, cur_time) 
    
# print(ANNONCEMENT(1,1,1,1).bitget_parser())

