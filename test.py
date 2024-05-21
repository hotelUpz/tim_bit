import requests
from bs4 import BeautifulSoup
get_location_link = 'https://2ip.ru'

proxy_host = '77.47.244.201'
proxy_port = '50100'
proxy_username = 'nikolassmsttt'
proxy_password = 'pRcwSxcJtT'

# proxy_url = f'http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}'
# proxiess = {
#     'http': proxy_url,
#     'https': proxy_url
# }

proxy_arg = f'nikolassmsttt:pRcwSxcJtT@77.47.244.201:50100'
# print(proxy_url)
proxiess = {
    "https": f"http://{proxy_arg}"
    # 'http': proxy_url,
    # 'https': proxy_url
}

# Пример запроса через прокси
try:
    response = requests.get('http://example.com', proxies=proxiess)
    print(response.text)
except requests.exceptions.ProxyError as e:
    print(f"Proxy error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")

try:
    response = requests.get(url=get_location_link, proxies=proxiess)
    soup = BeautifulSoup(response.text, 'lxml')
    ip = soup.find('div', class_ = 'ip').text.strip()
    location = soup.find('div', class_ = 'value-country').text.strip()
    print(ip, ':', location)

except Exception as ex:
    print(ex)
     


