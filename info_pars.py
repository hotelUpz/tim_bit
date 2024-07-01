import requests
from bs4 import BeautifulSoup
from joblib import Parallel, delayed
import time
from random import choice
from utils import UTILS, time_correction

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
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'origin': 'https://www.bitget.com/',
    'referer': 'https://www.bitget.com/',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',   
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'User-Agent': choice(user_agents)
}

class ANNONCEMENT(UTILS):
    def __init__(self) -> None:
        super().__init__()
        self.session = requests.Session()
        self.proxy_url = f'http://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}'
        self.proxiess = {
            'http': self.proxy_url,
            'https': self.proxy_url
        }

    def links_multiprocessor(self, data, cur_time, cpu_count=1): 
        total_list = []
        res = Parallel(n_jobs=cpu_count, prefer="threads")(delayed(lambda item: self.bitget_links_handler(item, cur_time))(item) for item in data)
        for x in res: 
            if x:               
                try:                    
                    total_list += x 
                except:
                    pass 
        return total_list

    def bitget_links_handler(self, data_item, cur_time):
        try:
            data_set = []
            notice_symbol = 'DMR'
            # bitget_headers['User-Agent'] = choice(user_agents)
            # print(bitget_headers)
            r = self.session.get(url=data_item['annUrl'], headers=bitget_headers, proxies=self.proxiess if self.is_proxies_true else None)
            # print(r)
            # print(r.text)
            soup = BeautifulSoup(r.text, 'html.parser')
            listing_time_all_potential_string = soup.find('div', class_='ArticleDetails_actice_details_main__oIjfu').get_text()
            trading_time_str = [x for x in listing_time_all_potential_string.split('\n') if "Trading Available:" in x][0].replace("Trading Available:", "").strip()
            # print(trading_time_str)
            listing_time = self.from_string_to_date_time(trading_time_str) 
            # print(listing_time) 
            # symbol_data = self.symbol_extracter(data_item['annTitle'])  
            # print(symbol_data)  
            if listing_time > cur_time - time_correction:
                # print(listing_time > cur_time - time_correction)
                symbol_data = self.symbol_extracter(data_item['annTitle'])  
                # print(symbol_data)   
                if symbol_data and not any(x for x in symbol_data if x == notice_symbol):
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
                 
    def bitget_parser(self):
        # print('Start parser')
        start_time = self.get_start_of_day()
        url = f"https://api.bitget.com/api/v2/public/annoucements?&annType=coin_listings&language=en_US"        
        r = self.session.get(url)
        # print(r)
        r_j = r.json()
        data = r_j["data"]        
        data = [{**x, "cTime": int(float(x["cTime"]))} for x in data if int(float(x["cTime"])) > start_time]
        # print(data)
        cur_time = int(time.time()* 1000)
        bitget_headers['User-Agent'] = choice(user_agents)
        return self.links_multiprocessor(data, cur_time) 

# proxy_host = '77.47.245.134'
# proxy_port = '59100'
# proxy_username = 'nikolassmsttt0Icgm'
# proxy_password = 'agrYpvDz7D'
    
# print(ANNONCEMENT(proxy_host, proxy_port, proxy_username, proxy_password).bitget_parser())

# [{'annId': '12560603810683', 'annTitle': 'New spot margin trading pair — ALICE/USDT!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810683', 'cTime': 1717487692000}, {'annId': '12560603810677', 'annTitle': 'Wealthy Tuesday #26: Enjoy an APR of up to 8.8% on USDT Earn product!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810677', 'cTime': 1717468248000}, {'annId': '12560603810614', 'annTitle': '[Initial Listing] Bitget Will List NexGami (NEXG) in the Innovation and Gamefi Zone.', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810614', 'cTime': 1717315200000}, {'annId': '12560603810613', 'annTitle': 'Bitget Will List pepe in a memes world (PEW) in the Innovation and MEME Zone.', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810613', 'cTime': 1717315257000}, {'annId': '12560603810624', 'annTitle': 'Notice on New Trading Pairs on Bitget Spot - 4 June 2024', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810624', 'cTime': 1717398015000}, {'annId': '12560603810632', 'annTitle': '[Initial Listing] Bitget Will List Ultiverse (ULTI) in the AI and Gamefi Zone!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810632', 'cTime': 1717412402000}, {'annId': '12560603810635', 'annTitle': 'Announcement of Bitget spot bot on adding GME/USDT', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810635', 'cTime': 1717406794000}, {'annId': '12560603810626', 'annTitle': 'Notice on Trading in Advance for DMR/USDT', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810626', 'cTime': 1717401642000}, {'annId': '12560603810618', 'annTitle': 'New spot margin trading pair — NOT/USDT!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810618', 'cTime': 1717385203000}, {'annId': '12560603810608', 'annTitle': 'Bitget Wealth Management concludes May with an APR of 10%', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810608', 'cTime': 1717236006000}, {'annId': '12560603810584', 'annTitle': 'Successful participants for Bitget TraderPro Season 2 - Batch 1', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810584', 'cTime': 1717154279000}, {'annId': '12560603810477', 'annTitle': 'Bitget Will List DeMR (DMR). Come and grab a share of $29,500 Worth of DMR!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810477', 'cTime': 1717142447000}, {'annId': '12560603810541', 'annTitle': 'New spot margin trading pair — DOG/USDT!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810541', 'cTime': 1717146317000}, {'annId': '12560603810540', 'annTitle': 'Announcement of Bitget spot bot on adding 3 new trading pairs', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810540', 'cTime': 1717125154000}]
