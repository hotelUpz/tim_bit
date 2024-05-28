import requests
from bs4 import BeautifulSoup
from joblib import Parallel, delayed
import time
from random import choice
from utils import UTILS, log_exceptions_decorator, time_correction

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
    def __init__(self, proxy_host, proxy_port, proxy_username, proxy_password) -> None:
        super().__init__()
        # print(proxy_host, proxy_port, proxy_username, proxy_password)
        self.session = requests.Session()
        self.session.mount('https://www.bitget.com', requests.adapters.HTTPAdapter(pool_connections=3, pool_maxsize=3))
        proxy_arg = f'{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}'    
        self.proxiess = {
            "https": f"http://{proxy_arg}"
            # 'http': proxy_url,
            # 'https': proxy_url
        }
        self.is_proxies_true = 0
    
    @log_exceptions_decorator
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
    # @log_exceptions_decorator
    def bitget_links_handler(self, data_item, cur_time):
        try:
            data_set = []
            # bitget_headers['User-Agent'] = choice(user_agents)
            # print(bitget_headers)
            r = self.session.get(url=data_item['annUrl'], headers=bitget_headers, proxies=self.proxiess if self.is_proxies_true else None)
            print(r)
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

# [{'annId': '12560603809830', 'annTitle': 'Bitget Will List VeChain (VET). Come and grab a share of $37,750 worth of VET!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809830', 'cTime': 1716202820000}, {'annId': '12560603810139', 'annTitle': 'Bitget Will List DOG (DOG) in the Innovation and BTC Ecosystem Zone!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810139', 'cTime': 1716458429000}, {'annId': '12560603810143', 'annTitle': 'Notice on New Trading Pairs on Bitget Spot - 24 May 2024', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810143', 'cTime': 1716465621000}, {'annId': '12560603810104', 'annTitle': 'Bitget pre-market trading: zkLink (ZKL) is set to launch soon', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810104', 'cTime': 1716447634000}, {'annId': '12560603809829', 'annTitle': 'Bitget Will List First Digital USD (FDUSD). Come and grab a share of $80,000 worth of FDUSD!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809829', 'cTime': 1716462007000}, {'annId': '12560603810140', 'annTitle': 'Bitget Will List SolarX (SXCH). Come and grab a share of $129,500 Worth SXCH!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810140', 'cTime': 1716465608000}, {'annId': '12560603810148', 'annTitle': '[Initial Listing] Bitget Will List Hiveswap (HIVP)', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810148', 'cTime': 1716469230000}, {'annId': '12560603810142', 'annTitle': 'Announcement on adjustment of position tier for BIGTIMEUSDT futures trading pair', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810142', 'cTime': 1716458432000}, {'annId': '12560603810107', 'annTitle': 'Bitget pre-market trading:Lista (LISTA) is set to launch soon', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810107', 'cTime': 1716447613000}, {'annId': '12560603809959', 'annTitle': '[Initial Listing] Bitget Will List Holograph (HLG). Come and grab a share of $89,000 worth of HLG!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809959', 'cTime': 1716292842000}, {'annId': '12560603810064', 'annTitle': 'BICOUSDT is Now Available on Futures', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810064', 'cTime': 1716451250000}, {'annId': '12560603810063', 'annTitle': 'HIFIUSDT is Now Available on Futures', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810063', 'cTime': 1716451256000}, {'annId': '12560603810106', 'annTitle': 'Bitget pre-market trading: Taiko (TKO) is set to launch soon', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810106', 'cTime': 1716447631000}, {'annId': '12560603810057', 'annTitle': 'Bitget PoolX is listing HashPack (PACK) : Stake USDT to mine PACK.', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810057', 'cTime': 1716385974000}, {'annId': '12560603810056', 'annTitle': 'Bitget PoolX is listing SaucerSwap (SAUCE): Stake BTC to mine SAUCE.', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810056', 'cTime': 1716385691000}, {'annId': '12560603809987', 'annTitle': 'Bitget pre-market trading: zkSync (ZKSYNC) is set to launch soon', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809987', 'cTime': 1716361215000}, {'annId': '12560603809998', 'annTitle': 'Bitget Crypto Loan Carnival: Borrow USDT, BTC, and ETH to enjoy an ultra-low interest rate of 1.2%', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809998', 'cTime': 1716375611000}, {'annId': '12560603810021', 'annTitle': '[Initial Listing] Bitget Will List MetaPhone (PHONE)', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603810021', 'cTime': 1716375612000}, {'annId': '12560603809977', 'annTitle': 'Exclusive ETH saving campaign for African Users : 20% APR!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809977', 'cTime': 1716363926000}, {'annId': '12560603809902', 'annTitle': 'Bitget Will List SaucerSwap (SAUCE). Come and grab a share of 998,000 SAUCE!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809902', 'cTime': 1716292819000}, {'annId': '12560603809901', 'annTitle': '[Initial Listing] Bitget Will List HashPack (PACK). Come and grab a share of 7,083,000 PACK!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809901', 'cTime': 1716292856000}, {'annId': '12560603809810', 'annTitle': '[Initial Listing] Bitget Will List NYAN (NYAN)', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809810', 'cTime': 1716184842000}, {'annId': '12560603809831', 'annTitle': '[Initial Listing] Bitget Will List Thetanuts Finance (NUTS). Come and grab a share of 1,266,666 NUTS!', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809831', 'cTime': 1716195621000}, {'annId': '12560603809836', 'annTitle': 'Bitget PoolX is listing Thetanuts Finance (NUTS) : Stake BGB to mine NUTS', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809836', 'cTime': 1716188400000}, {'annId': '12560603809821', 'annTitle': 'Bitget pre-market trading:Layerzero(ZRO) is set to launch soon', 'annDesc': '产品更新&新币上线', 'language': 'en_US', 'annUrl': 'https://www.bitget.com/en/support/articles/12560603809821', 'cTime': 1716177648000}]

