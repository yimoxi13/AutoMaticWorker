import requests
from lxml import etree
import json
import getpass


def get_ticketId(html_text):
    root = etree.HTML(html_text)
    script_element = root.xpath('//script[contains(text(), "ticketId")]')[0]
    script_text = script_element.text.strip()
    start_index = script_text.find('"ticketId": "') + len('"ticketId": "')
    end_index = script_text.find('"', start_index)
    ticketId = script_text[start_index:end_index]
    return ticketId


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


print("请输入用户名和密码， 密码不可见是正常情况")
print("此处未做登录成功验证， 如果运行失败请自行检查用户密码是否正确")
password = input("输入用户名并回车:")
username = getpass.getpass("请输入密码并回车:")
user = User(password, username)

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
ticket_id = get_ticketId(response.text)
print("返回的tickit:", ticket_id)
cookies = response.cookies
print("返回的Cookie:", cookies)

cookies_list = [{'name': cookie.name, 'value': cookie.value} for cookie in cookies]

data_dict = [{
    "user": user.username,
    "cookies": cookies_list,
    "ticket": ticket_id
}]

with open('user_auth.json', 'w') as f:
    json.dump(data_dict, f)
    input("保存完成，输入任意内容关闭...")
