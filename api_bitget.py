from hashlib import sha256
import hmac
import base64
import json
import time
import requests
from urllib.parse import urlencode
from log import Total_Logger
import os
import inspect
current_file = os.path.basename(__file__) #

class BITGET_API(Total_Logger):
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.bitget.com"
        self.orders_endpoint = "/api/v2/spot/trade/place-order"
        self.orders_url = self.base_url + self.orders_endpoint
        self.order_data_endpoint = "/api/v2/spot/trade/orderInfo"
        self.session = requests.Session()
                
    # POST ////////////////////////////////////////////////////////////////////
    def generate_post_signature_bitget(self, timestamp, endpoint, payload):
        message = timestamp + 'POST' + endpoint + json.dumps(payload)
        signature = base64.b64encode(hmac.new(self.api_secret.encode('utf-8'), message.encode('utf-8'), sha256).digest())
        return signature
        
    def get_post_params(self, symbol, side, size, target_price, market_type):
        # print(symbol, side, size, target_price, market_type)
        timestamp = str(self.test_listing_time_ms + self.incriment_time_ms) if side == 'BUY' else str(int(time.time() * 1000))
        # timestamp = str(int(time.time() * 1000))
        payload = {
            "symbol": symbol,
            "side": side,
            "orderType": market_type,
            "size": str(size)
        }
        if market_type == 'limit':
            payload['price'] = str(target_price)
            payload['force'] = 'gtc'
        payload = {str(key): value for key, value in payload.items()}
        headers = {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": self.generate_post_signature_bitget(timestamp, self.orders_endpoint, payload),
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.api_passphrase,
            "Content-Type": "application/json",
            "locale": "en-US"
        }
        return payload, headers
    
    
    def place_market_order(self, symbol, side, size):        
        market_type = 'market'
        targetprice = None
        payload, headers = self.get_post_params(symbol, side, size, targetprice, market_type)
        resp = self.session.post(self.orders_url, headers=headers, json=payload) 
        return resp

     # /////////////////////////////////////////////////////////////////////////
    def send_fake_request(self, fake_sumbol):
        response = self.place_market_order(fake_sumbol, 'BUY', 7)    
        print("First request!")            
        self.cookies = response.cookies
        self.session.cookies.update(self.cookies)
    # /////////////////////////////////////////////////////////////////////////
    #  GET //////////////////////////////////////////////////////////////////
    def sign_order_data_bitget(self, message, secret_key):
        mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        return base64.b64encode(mac.digest()).decode()

    def pre_hash(self, timestamp, method, request_path, body):
        return timestamp + method.upper() + request_path + body
    
    
    def get_order_data(self, orderId):
        timestamp = str(int(time.time() * 1000))        
        params = {"orderId": orderId}
        request_path = self.order_data_endpoint + '?' + urlencode(sorted(params.items()))
        body = ""
        message = self.pre_hash(timestamp, "GET", request_path, body)
        signature = self.sign_order_data_bitget(message, self.api_secret)
        headers = {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.api_passphrase,
            "Content-Type": "application/json",
            "locale": "en-US"
        }
        return self.session.get(self.base_url + request_path, headers=headers)      

    
    def get_balance(self, symbol):

        timestamp = str(int(time.time() * 1000)) 
        params = {
            "coin": symbol
        }     
        request_path = '/api/v2/spot/account/bills' + '?' + urlencode(sorted(params.items()))
        body = ""
        message = self.pre_hash(timestamp, "GET", request_path, body)
        signature = self.sign_order_data_bitget(message, self.api_secret)
        headers = {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.api_passphrase,
            "Content-Type": "application/json",
            "locale": "en-US"
        }
        return requests.get(self.base_url + request_path, headers=headers)        
