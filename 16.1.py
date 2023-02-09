'''
Description:
Author: CaoShiWei
Date: 2022-11-07 14:18:32
LastEditTime: 2022-11-22 09:02:59
LastEditors:  
'''
# -- coding:UTF-8 --
import requests  # 导入模块
from lxml import etree
from fake_useragent import UserAgent
import json
# 简单的反爬，设置一个请求头来伪装成浏览器

# python内置的微型浏览器，没有界面的
# 作用：缓存cookies
s = requests.session()
# print(s.headers)
# #伪造请求头部，伪装成从真实浏览器发出的请求
h = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
}
s.headers.update(h)
# print(s.headers)
# exit(0)


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


# request_header()
# exit()
'''
创建两个列表用来存放代理ip
'''
all_ip_list = []  # 用于存放从网站上抓取到的ip
usable_ip_list = []  # 用于存放通过检测ip后是否可以使用

# 发送请求，获得响应


def send_request():
    # 爬取7页，可自行修改
    # for i in range(1, 8):
    # print(f'正在抓取第{i}页……')
    response = requests.get(
        url=f'https://www.proxy-list.download/api/v2/get?l=en&t=http', headers=request_header())
    # text = response.text.encode('ISO-8859-1')
    j = json.loads(response.text)
    tr_list = j['LISTA']

    # print(j['LISTA'])
    # print(type(tr_list))
    # exit(0)
    # 使用xpath解析，提取出数据ip，端口
    # html = etree.HTML(text)
    # tr_list = html.xpath('/html/body/div[2]/div/div[2]/table/tbody/tr')
    for td in tr_list:
        # print(td)
        ip_ = td['IP']
        port_ = td['PORT']
        proxy = ip_ + ':' + port_  # 115.218.5.5:9000

        all_ip_list.append(proxy)
        # print(proxy)

        # test_ip(proxy)  # 开始检测获取到的ip是否可以使用
        # if proxy == test_ip(proxy):

        #     return proxy
        # ip_ = td.xpath('./td[1]/text()')[0]  # ip
        # port_ = td.xpath('./td[2]/text()')[0]  # 端口
        proxy = ip_ + ':' + port_  # 115.218.5.5:9000
        test_ip(proxy)  # 开始检测获取到的ip是否可以使用
    print('抓取完成！')
    print(f'抓取到的ip个数为：{len(all_ip_list)}')
    print(f'可以使用的ip个数为：{len(usable_ip_list)}')
    print('分别有：\n', usable_ip_list)
# 检测ip是否可以使用


def test_ip(proxy, url="https://www.dianping.com/shop/G7Yc9UhIsKP88luu"):
    # 构建代理ip
    proxies = {
        "http": "http://" + proxy,
        "https": "http://" + proxy,
        # "http": proxy,
        # "https": proxy,
    }
    try:
        response = requests.get(url=url, headers=request_header(),
                                proxies=proxies, timeout=1)  # 设置timeout，使响应等待1s
        # response.close()#请求关闭
        if response.status_code == 200:
            # print(proxy)
            # return proxy
            usable_ip_list.append(proxy)
            print(proxy, '\033[31m可用\033[0m')
        else:
            print(proxy, '不可用')
    except:
        print(proxy, '请求异常')


if __name__ == '__main__':
    proxy = send_request()
    print(11)
    print(proxy)
