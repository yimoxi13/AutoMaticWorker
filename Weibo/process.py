# Copyright (c) 2024 Adroke@163.com
#
# 本文件受版权法保护，所有权利保留。
# 本文件并非依据 MIT 开源协议发布。未经版权所有者书面许可，
# 禁止在未经授权的情况下以任何形式（包括但不限于复制、分发、修改、衍生作品创建等）使用、传播本代码。

import requests
import json
import sys

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class TaskInfo:
    def __init__(self):
        self.casi_case_id = None
        self.ticket_id = None
        self.withhold_id = None
        self.loan_voucher_id = None
        self.loan_debtor_name = None
        self.message = None
    
    def __str__(self):
        return f"casi_case_id: {self.casi_case_id}, ticket_id: {self.ticket_id}"
    
    def set_casi_case_id(self, casi_case_id):
        self.casi_case_id = casi_case_id
    
    def set_ticket_id(self, ticket_id):
        self.ticket_id = ticket_id
        
    def set_withhold_id(self, withhold_id):
        self.withhold_id = withhold_id
    
    def set_loan_voucher_id(self, loan_voucher_ids):
        self.loan_voucher_ids = loan_voucher_ids
    
    def set_loan_debtor_name(self, loan_debtor_name):
        self.loan_debtor_name = loan_debtor_name
        
    def set_message(self, message):
        self.message = message
        
    def get_casi_case_id(self):
        return self.casi_case_id
    
    def get_ticket_id(self):
        return self.ticket_id
    
    def get_withhold_id(self):
        return self.withhold_id
    
    def get_loan_debtor_name(self):
        return self.loan_debtor_name
    
    def get_loan_voucher_id(self):
        return self.loan_voucher_id
    
    def get_message(self):
        return self.message

def search_cookie_for_user(cookie_file_name, target_user):
    with open(cookie_file_name, 'r') as f:
        json_data = json.load(f)

    for item in json_data:
        if item['user'] == target_user:
            return item['cookies']

    return None

def convert_cookies_to_jar(cookies_list):
    cookie_jar = requests.cookies.RequestsCookieJar()
    for cookie in cookies_list:
        cookie_jar.set(cookie['name'], cookie['value'])
    return cookie_jar

def update_case_info(session, phone_number, task_info: TaskInfo):
    page_api = "https://amls-legal.sinaft.com/amls/casix/casixCaseDispose/list/result/page"
    form_data = {
        "funcType": "201056",
        "casixRevokeNoticeIdByBefore": "",
        "disposeTeamId": "",
        "edpdLoanDebtorId": "",
        "phoneM4Encry": phone_number,
        "edpdContLoanSignPlatformId": "",
        "edpdContLoanCreditorId": "",
        "edpdAoccCreditorId": "",
        "overdueDaysStart": "",
        "overdueDaysEnd": "",
        "edpdVoucherOverdueAmtStart": "",
        "edpdVoucherOverdueAmtEnd": "",
        "entrustDateStart": "",
        "entrustDateEnd": "",
        "entrustDaysStart": "",
        "entrustDaysEnd": "",
        "flowUpDaysStart": "",
        "flowUpDaysEnd": "",
        "noFllowUpDaysStart": "",
        "noFllowUpDaysEnd": "",
        "lastFlowUpTimeStart": "",
        "lastFlowUpTimeEnd": "",
        "entrustStatus": ""
    }
    page_headers = {
        "Accept": "text/html, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "455",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "amls-legal.sinaft.com",
        "Origin": "https://portal-legal.sinaft.com",
        "Platform-Params": "ticketId=BB95751B59AC49AEBE2786BC516F8B1A",
        "Referer": "https://portal-legal.sinaft.com/login.xhtml",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }
    # TODO: 记得做网络错误处理, 将导致空值的错误抛出
    response = session.post(page_api, data=form_data, headers=page_headers)
    response.encoding = "UTF-8"
    json_data = json.loads(response.text)
    
    print(json_data)
    
    business_data = json_data["business"]
    pagination_data = business_data["pagination"]
    data_list = pagination_data["data"]
    
    casiCaseId = data_list[0]["casiCaseId"]

    extMap = pagination_data["extMap"]
    entity = extMap["entity"]
    extAttrMap = entity["extAttrMap"]
    
    ticketId = extAttrMap["ticketId"]
    
    print("casiCaseId的值为:", casiCaseId)
    print("ticketId的值为:", ticketId)
    
    task_info.set_casi_case_id(casiCaseId)
    task_info.set_ticket_id(ticketId)
    return True

def update_business_info(session, task_info: TaskInfo):
    case_api = "https://edpd-legal.sinaft.com/edpd/casi/casiCase/queryCaseInfo"
    case_headers = {
        "Accept": "text/html, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "0",
        "Host": "edpd-legal.sinaft.com",
        "Origin": "https://portal-legal.sinaft.com",
        "Platform-Params": f"ticketId={task_info.ticket_id}",
        "Referer": "https://portal-legal.sinaft.com/login.xhtml",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }

    form_data = {
        "casiCaseId": task_info.casi_case_id
        }

    # TODO: 记得做网络错误处理, 将导致空值的错误抛出
    response = session.post(case_api, data=form_data, headers=case_headers)
    json_data = json.loads(response.text)
    print(json_data)
    
    business = json_data["business"]
    withholdId = business["id"]
    loanDebtorName = business["loanDebtorName"]
    extAttrMap = business["extAttrMap"]
    loanVoucherIds = extAttrMap["loanVoucherIds"]

    print("bussinessId:", withholdId)
    print("loanVoucherIds:", loanVoucherIds)
    print("loanDebtorName:", loanDebtorName)
    
    task_info.set_withhold_id(withholdId)
    task_info.set_loan_debtor_name(loanDebtorName)
    task_info.set_loan_voucher_id(loanVoucherIds)
    
    return True

def do_withhold(session, task_info: TaskInfo):
    withhold_api = "https://edpd-legal.sinaft.com/edpd/casi/casiRepayWithholdFlow/withholdApply"

    form_data = {
        "id": task_info.withhold_id,
        "loanVoucherIds": task_info.loan_voucher_ids,
        }
    withhold_headers = {
        "Accept": "text/html, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Length": "0",
        "Host": "edpd-legal.sinaft.com",
        "Origin": "https://portal-legal.sinaft.com",
        "Platform-Params": f"ticketId={task_info.ticket_id}",
        "Referer": "https://portal-legal.sinaft.com/login.xhtml",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }
    
    # TODO: 记得做网络错误处理, 将导致空值的错误抛出
    response = session.post(withhold_api, data=form_data, headers=withhold_headers)
    print(response.text)
    json_data = json.loads(response.text)
    task_info.message = json_data["resp"]["message"]
    
    return True

if __name__ == "__main__":
    user = User("baorunM6", "123456Abc#")
    cookie_file_name = "user_auth.json"
    session = requests.Session()

    cookies_list = search_cookie_for_user(cookie_file_name, user.username)
    
    if cookies_list:
        cookies_jar = convert_cookies_to_jar(cookies_list)
    else:
        print(f"未找到用户 {user.username} 的cookie。")
        sys.exit()  # TODO: 错误处理
        
    session.cookies.update(cookies_jar)
    
    # TODO: 实现读取多个电话号码的功能
    phone_numbers = ["电话号码1", "电话号码2"]
    for phone_number in phone_numbers:
        task_info = TaskInfo()
        
        is_update_case = update_case_info(session, "电话号码", task_info)
        is_update_business = update_business_info(session, task_info)
        is_withhold = do_withhold(session, task_info)
        
        print(f"{task_info.get_loan_debtor_name}操作结果: {task_info.get_message}")
        
        
                