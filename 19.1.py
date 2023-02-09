'''
Description: 
Author: 
Date: 2023-01-12 16:02:55
LastEditTime: 2023-01-12 16:04:13
LastEditors:  
'''
import requests

# 登录
url = "https://wapi.http.linkudp.com/index/users/login_do"
body = {
'phone': '17303169207',
'password': '7710586zxc',
'remember': '0'
}
headers = {
"Accept": "text/html, */*; q=0.01",
"Accept-Encoding": 'gzip, deflate, br',
"Accept-Language": 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'Content-Length': '48',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Host': 'wapi.http.linkudp.com',
"Origin": 'https://www.zmhttp.com',
"Referer": 'https://www.zmhttp.com/',
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'cross-site',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}
response = requests.post(url, json=body, headers=headers)
print(response.text)
result=response.json()
print(result['ret_data'])

# 获取用户信息
url="https://wapi.http.linkudp.com/index/users/user_info"
body = {

}
headers = {
"Accept": "text/html, */*; q=0.01",
"Accept-Encoding": 'gzip, deflate, br',
"Accept-Language": 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'Content-Length': '0',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Host': 'wapi.http.linkudp.com',
"Origin": 'https://www.zmhttp.com',
"Referer": 'https://www.zmhttp.com/ucenter/?first_time=0',
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'cross-site',
'session-id': result['ret_data'],
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}
response = requests.post(url, json=body, headers=headers)
print(response.text)

#自动领取每日免费ip
url = "https://wapi.http.linkudp.com/index/users/get_day_free_pack"
body = {
'geetest_challenge': '',
'geetest_validate': '',
'geetest_seccode': ''
}
headers = {
"Accept": "text/html, */*; q=0.01",
"Accept-Encoding": 'gzip, deflate, br',
"Accept-Language": 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'Content-Length': '53',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Host': 'wapi.http.linkudp.com',
"Origin": 'https://www.zmhttp.com',
"Referer": 'https://www.zmhttp.com/ucenter/?first_time=0',
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'cross-site',
'session-id': result['ret_data'],
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}
response = requests.post(url, json=body, headers=headers)
print(response.text)


