import requests
import json

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
user = User("baorunM6", "123456Abc#")
login_url = "https://portal-legal.sinaft.com/login.xhtml"
cookies = ""
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Length": "70",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": cookies,
    "Host": "portal-legal.sinaft.com",
    "Origin": "https://portal-legal.sinaft.com",
    "Referer": "https://portal-legal.sinaft.com/login.xhtml",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36",
    "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"'
}

form_data = {
    "loginType": "pwd",
    "loginChannel": "pc",
    "loginName": user.username,
    "password": user.password
    }

response = requests.post(login_url, data=form_data, headers=headers)
cookies = response.cookies
print("返回的Cookie:", cookies)

cookies_list = [{'name': cookie.name, 'value': cookie.value} for cookie in cookies]

data_dict = [{
    "user": user.username,
    "cookies": cookies_list
    }]

with open('user_auth.json', 'w') as f:
    json.dump(data_dict, f)
    print("保存完成")

