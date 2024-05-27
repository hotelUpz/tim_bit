from hashlib import sha256
import hmac
import base64
import json
import time
import requests
from urllib.parse import urlencode
from parametrs import PARAMS
from utils import log_exceptions_decorator

class BITGET_API(PARAMS):
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.bitget.com"
        self.orders_endpoint = "/api/v2/spot/trade/place-order"
        self.orders_url = self.base_url + self.orders_endpoint
        self.order_data_endpoint = "/api/v2/spot/trade/orderInfo"
        self.session = requests.Session()
                
    # POST ////////////////////////////////////////////////////////////////////
    @log_exceptions_decorator
    def generate_post_signature_bitget(self, timestamp, endpoint, payload):
        message = timestamp + 'POST' + endpoint + json.dumps(payload)
        signature = base64.b64encode(hmac.new(self.api_secret.encode('utf-8'), message.encode('utf-8'), sha256).digest())
        return signature

    @log_exceptions_decorator    
    def get_post_params(self, symbol, side, size, target_price, market_type):
        # print(symbol, side, size, target_price, market_type)
        timestamp = str(self.listing_time_ms + self.incriment_time_ms) if side == 'BUY' else str(int(time.time() * 1000))
        # timestamp = str(int(time.time() * 1000))
        payload = {
            "symbol": symbol,
            "side": side,
            "orderType": market_type,
            "size": str(size),
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
    
    @log_exceptions_decorator
    def place_market_order(self, symbol, side, size):        
        market_type = 'market'
        targetprice = None
        payload, headers = self.get_post_params(symbol, side, size, targetprice, market_type)
        return self.session.post(self.orders_url, headers=headers, json=payload)

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
    
    @log_exceptions_decorator
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

# {'code': '00000', 'msg': 'success', 'requestTime': 1715598961792, 'data': [{'userId': '5604086735', 'symbol': 'ARBUSDT', 'orderId': '1173872613484412935', 'clientOid': '75eac07f-7d86-4209-bda6-d4c364cefd97', 'price': '0', 'size': '10', 'orderType': 'market', 'side': 'buy', 'status': 'filled', 'priceAvg': '0.9911100000000000', 'baseVolume': '10.08', 'quoteVolume': '9.9903888000000000', 'enterPointSource': 'API', 'feeDetail': '{"newFees":{"c":0,"d":0,"deduction":false,"r":-0.01008,"t":-0.01008,"totalDeductionFee":0},"ARB":{"deduction":false,"feeCoinCode":"ARB","totalDeductionFee":0,"totalFee":-0.0100800000000000}}', 'orderSource': 'market', 'tpslType': 'normal', 'triggerPrice': None, 'quoteCoin': 'USDT', 'baseCoin': 'ARB', 'cTime': '1715598961230', 'uTime': '1715598961334'}]}
      
