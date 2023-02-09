'''
Description: 
Author: CaoShiWei
Date: 2022-11-21 15:30:41
LastEditTime: 2022-11-24 17:41:37
LastEditors:  
'''
# -- coding:UTF-8 --
import requests  # 导入模块
from lxml import etree
from fake_useragent import UserAgent
import json
# 简单的反爬，设置一个请求头来伪装成浏览器
s = requests.session()
# print(s.headers)
# #伪造请求头部，伪装成从真实浏览器发出的请求
h = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
}
s.headers.update(h)


def request_header():
    headers = {
        # 'User-Agent': UserAgent().random #常见浏览器的请求头伪装（如：火狐,谷歌）
        'User-Agent': UserAgent().Chrome  # 谷歌浏览器
    }
    # print(type(UserAgent()))
    # for i in UserAgent:
    #     print(i)
    # print(headers)
    return headers


def send_request(url):
    response = requests.get(
        url=f'http://http.tiqu.letecs.com/getip3?num=2&type=1&pro=&city=0&yys=0&port=1&pack=252474&ts=0&ys=0&cs=0&lb=6&sb=,&pb=4&mr=1&regions=', headers=request_header())
    j = response.text
    # j = json.loads(response.text)
    # print(type(j))
    # print(j)
    tr_list = j.split(',')
    for td in tr_list:

        proxy = td  # 115.218.5.5:9000
        test_ip(proxy, url)  # 开始检测获取到的ip是否可以使用
        if proxy == test_ip(proxy, url):
            return proxy


def test_ip(proxy, url="http://www.woman91.com/"):
    # 构建代理ip         http://www.woman91.com/
    proxies = {
        "http": "http://" + proxy,
        "https": "http://" + proxy,
    }
    try:
        response = requests.get(url=url, headers=request_header(),
                                proxies=proxies, timeout=1)  # 设置timeout，使响应等待1s
        if response.status_code == 200:
            # print(proxy)
            return proxy

    except:
        # print(proxy)
        # if str(proxy).split(':')[1] == '121' or str(proxy).split(':')[1] == '115':
        #     return proxy  # 121今日套餐已用完  115 套餐已过期
        # else:
        print(proxy, '请求异常')


pr = send_request(url="http://www.shenzhen91.com/")
# # # p = pr.split(':')

# if pr == '{"code":121' or pr == '{"code":115':
#     print(11)
# proxy = '8.141.251.188:3128'
# # test_ip(proxy)
# if test_ip(proxy) == proxy:
#     print(proxy)
# proxy = 1
# i=0

# while 5 != proxy or i==2:
#     i=i+1
#     proxy = proxy+1
#     # proxies = {
#     #     "http": "http://" + proxy,
#     #     "https": "http://" + proxy,
#     # }
#     print(i)
#     print(proxy)

# print(i)
# print(proxy)
# print(pr.split(':')[1])
# # print(type(pr))
