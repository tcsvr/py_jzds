#-- coding:UTF-8 --
# 竞争对手数据分析后台系统(数据存入 数据库)
from cgi import print_arguments
from cmd import IDENTCHARS
from re import T
import requests
import parsel
# import csv
from bs4 import BeautifulSoup
from urllib import parse
from urllib.parse import urlparse
from scrapy import Selector
import json
import mysql.connector
import re
import random
from fake_useragent import UserAgent
# 通过re过滤除中英文及数字以外的其他字符


def filter_string(des_string, re_string=''):
    res = re.compile("[^\\u4e00-\\u9fa5^a-z^A-Z^0-9]")
    return res.sub(re_string, des_string)


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="is_shenzhen90_com"
    # database="is_sz"
)
# 竞争对手数据分析后台系统



mycursor = mydb.cursor()



url_list=[
    'https://www.dianping.com/search/keyword/7/0_%E7%BE%8E%E5%AE%B9/o9p12',
    # 'https://www.dianping.com/search/keyword/7/0_%E7%BE%8E%E5%AE%B9/o9p13',
]

for url in url_list:
    # id = ur[0]
    # url = ur[1]
    print(url)


    headers = [
            {
            'Host': 'www.dianping.com',
            'Referer': 'https://www.dianping.com/search/keyword/7/0_%E7%BE%8E%E5%AE%B9/o9p12',
            'User-Agent':UserAgent().Chrome,
            "Cookie": '__mta=245675963.1667553086131.1667553086131.1667553086131.1; cy=7; cityid=7; cye=shenzhen; _lxsdk_cuid=182d2e7a87376-0263598e1d211a-3b3d5203-1fa400-182d2e7a875c8; _lxsdk=182d2e7a87376-0263598e1d211a-3b3d5203-1fa400-182d2e7a875c8; _hc.v=fca25476-1075-20dc-e29a-ed63d2b3c436.1661395775; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1666682005; s_ViewType=10; WEBDFPID=v3y1vz815vv655vu0yzz49865368w5x081558v48zv7979587u7w5z08-1982912843054-1667552842511CKEUMOIfd79fef3d01d5e9aadc18ccd4d0c95072773; aburl=1; dplet=9751085cb4ee13d465b7d7b5bcc852a1; dper=1632cd81f4b05219e116fe2e1a07f65283da2f59b104849aba3d6b526500a86004c64e1dbc476d0a0ddc9c6b22abc39a0cb87b8a139e335b5ef79f19e29ba6953d67f4515c2dac7577993aedaafd6709d6d181ad6a49f819b71efa3dfed2137c; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_3476436004; ctu=70159c3dea4054244f82221ceea4a625da1342f6106402faaf6ee6af7df83a9f; fspop=test; cy=2; cye=beijing; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1668042166; _lxsdk_s=1846075af41-4a2-0ea-3d4%7C%7C1'
            },
            {
            'Host': 'www.dianping.com',
            'Referer': 'https://www.dianping.com/search/keyword/7/0_%E7%BE%8E%E5%AE%B9/o9p12',
            'User-Agent':UserAgent().Chrome,
            "Cookie": '__mta=245675963.1667553086131.1667553086131.1667553086131.1; cy=1; cityid=1; cye=shanghai; _lxsdk_cuid=182d2e7a87376-0263598e1d211a-3b3d5203-1fa400-182d2e7a875c8; _lxsdk=182d2e7a87376-0263598e1d211a-3b3d5203-1fa400-182d2e7a875c8; _hc.v=fca25476-1075-20dc-e29a-ed63d2b3c436.1661395775; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1666682005; s_ViewType=10; WEBDFPID=v3y1vz815vv655vu0yzz49865368w5x081558v48zv7979587u7w5z08-1982912843054-1667552842511CKEUMOIfd79fef3d01d5e9aadc18ccd4d0c95072773; aburl=1; ctu=70159c3dea4054244f82221ceea4a625da1342f6106402faaf6ee6af7df83a9f; fspop=test; cy=2; cye=beijing; _lxsdk_s=1846075af41-4a2-0ea-3d4%7C%7C56; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1668065914'
            },{
                'Host': 'mapi.dianping.com',
                'Referer': 'mapi.dianping.com',
                'User-Agent':UserAgent().firefox,
                # 'User-Agent':UserAgent().Chrome,
                # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                "Cookie": 'cy=1; cityid=1; cye=shanghai; _lxsdk_cuid=18407d265b220-02df1e3ca332668-4076032e-1fa400-18407d265b4c8; _lxsdk=18407d265b220-02df1e3ca332668-4076032e-1fa400-18407d265b4c8; _hc.v=b7d2b53a-4bba-c0d1-8e4c-e3895822e059.1666578540; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1666578540,1667871521; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1668065522; WEBDFPID=8304u1vx37845z44y9030v61zw0vxv6z815448v1u1v97958y645z7z9-1983235374873-1667875373425WWIWICO10f02007e9804b0b4cf483cebf1f9f519412; s_ViewType=10; fspop=test; cy=7; cye=shenzhen; dplet=a46f6d036e6cdca18e55bb4eb824de74; dper=1632cd81f4b05219e116fe2e1a07f65202602f2aa515177b56a547153984aa9d6fc4a80806c2610bc26308e07a3fff02fd70c179c1e163959cb761cf4486da8b47dec6b3c9f0e34ab52a53636423b00ac97fc5c4c7e36a9c79e3182b2db7c58d; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_3476436004; ctu=70159c3dea4054244f82221ceea4a625a0e4b97b8d4194192729d58089ece748; _lxsdk_s=1846073e3bc-67d-e2d-561%7C%7C7'

            },{
                'Host': 'mapi.dianping.com',
                'Referer': 'mapi.dianping.com',
                'User-Agent':UserAgent().firefox,
                # 'User-Agent':UserAgent().Chrome,
                # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                "Cookie": 'cy=1; cityid=1; cye=shanghai; _lxsdk_cuid=18407d265b220-02df1e3ca332668-4076032e-1fa400-18407d265b4c8; _lxsdk=18407d265b220-02df1e3ca332668-4076032e-1fa400-18407d265b4c8; _hc.v=b7d2b53a-4bba-c0d1-8e4c-e3895822e059.1666578540; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1666578540,1667871521; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1668066063; WEBDFPID=8304u1vx37845z44y9030v61zw0vxv6z815448v1u1v97958y645z7z9-1983235374873-1667875373425WWIWICO10f02007e9804b0b4cf483cebf1f9f519412; s_ViewType=10; fspop=test; cy=7; cye=shenzhen; ctu=70159c3dea4054244f82221ceea4a625a0e4b97b8d4194192729d58089ece748; _lxsdk_s=1846073e3bc-67d-e2d-561%7C%7C14'

            }
        ]

    headers1 = [
            {
            'Host': 'www.dianping.com',
            'Referer': 'https://www.dianping.com/search/keyword/7/0_%E7%BE%8E%E5%AE%B9/o9p12',
            'User-Agent':UserAgent().Chrome,
            "Cookie": '_lxsdk_cuid=182d2e7a87376-0263598e1d211a-3b3d5203-1fa400-182d2e7a875c8; _lxsdk=182d2e7a87376-0263598e1d211a-3b3d5203-1fa400-182d2e7a875c8; _hc.v=fca25476-1075-20dc-e29a-ed63d2b3c436.1661395775; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1666682005; s_ViewType=10; WEBDFPID=v3y1vz815vv655vu0yzz49865368w5x081558v48zv7979587u7w5z08-1982912843054-1667552842511CKEUMOIfd79fef3d01d5e9aadc18ccd4d0c95072773; aburl=1; dplet=9751085cb4ee13d465b7d7b5bcc852a1; dper=1632cd81f4b05219e116fe2e1a07f65283da2f59b104849aba3d6b526500a86004c64e1dbc476d0a0ddc9c6b22abc39a0cb87b8a139e335b5ef79f19e29ba6953d67f4515c2dac7577993aedaafd6709d6d181ad6a49f819b71efa3dfed2137c; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_3476436004; ctu=70159c3dea4054244f82221ceea4a625da1342f6106402faaf6ee6af7df83a9f; fspop=test; cy=2; cye=beijing; _lxsdk_s=1846075af41-4a2-0ea-3d4%7C%7C2; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1668065708'
            },{
            'Host': 'www.dianping.com',
            'Referer': 'https://www.dianping.com/search/keyword/7/0_%E7%BE%8E%E5%AE%B9/o9p12',
            'User-Agent':UserAgent().Chrome,
            "Cookie": '_lxsdk_cuid=182d2e7a87376-0263598e1d211a-3b3d5203-1fa400-182d2e7a875c8; _lxsdk=182d2e7a87376-0263598e1d211a-3b3d5203-1fa400-182d2e7a875c8; _hc.v=fca25476-1075-20dc-e29a-ed63d2b3c436.1661395775; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1666682005; s_ViewType=10; WEBDFPID=v3y1vz815vv655vu0yzz49865368w5x081558v48zv7979587u7w5z08-1982912843054-1667552842511CKEUMOIfd79fef3d01d5e9aadc18ccd4d0c95072773; aburl=1; ctu=70159c3dea4054244f82221ceea4a625da1342f6106402faaf6ee6af7df83a9f; fspop=test; cy=2; cye=beijing; _lxsdk_s=1846075af41-4a2-0ea-3d4%7C%7C57; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1668065989'
            },{
                'Host': 'mapi.dianping.com',
                'Referer': 'mapi.dianping.com',
                'User-Agent':UserAgent().firefox,
                # 'User-Agent':UserAgent().Chrome,
                # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                "Cookie": '_lxsdk_cuid=18407d265b220-02df1e3ca332668-4076032e-1fa400-18407d265b4c8; _lxsdk=18407d265b220-02df1e3ca332668-4076032e-1fa400-18407d265b4c8; _hc.v=b7d2b53a-4bba-c0d1-8e4c-e3895822e059.1666578540; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1666578540,1667871521; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1668065781; WEBDFPID=8304u1vx37845z44y9030v61zw0vxv6z815448v1u1v97958y645z7z9-1983235374873-1667875373425WWIWICO10f02007e9804b0b4cf483cebf1f9f519412; s_ViewType=10; fspop=test; cy=7; cye=shenzhen; dplet=a46f6d036e6cdca18e55bb4eb824de74; dper=1632cd81f4b05219e116fe2e1a07f65202602f2aa515177b56a547153984aa9d6fc4a80806c2610bc26308e07a3fff02fd70c179c1e163959cb761cf4486da8b47dec6b3c9f0e34ab52a53636423b00ac97fc5c4c7e36a9c79e3182b2db7c58d; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_3476436004; ctu=70159c3dea4054244f82221ceea4a625a0e4b97b8d4194192729d58089ece748; _lxsdk_s=1846073e3bc-67d-e2d-561%7C%7C8'

            },{
                'Host': 'mapi.dianping.com',
                'Referer': 'mapi.dianping.com',
                'User-Agent':UserAgent().firefox,
                # 'User-Agent':UserAgent().Chrome,
                # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                "Cookie": '_lxsdk_cuid=18407d265b220-02df1e3ca332668-4076032e-1fa400-18407d265b4c8; _lxsdk=18407d265b220-02df1e3ca332668-4076032e-1fa400-18407d265b4c8; _hc.v=b7d2b53a-4bba-c0d1-8e4c-e3895822e059.1666578540; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1666578540,1667871521; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1668066408; WEBDFPID=8304u1vx37845z44y9030v61zw0vxv6z815448v1u1v97958y645z7z9-1983235374873-1667875373425WWIWICO10f02007e9804b0b4cf483cebf1f9f519412; s_ViewType=10; fspop=test; cy=7; cye=shenzhen; ctu=70159c3dea4054244f82221ceea4a625a0e4b97b8d4194192729d58089ece748; _lxsdk_s=1846073e3bc-67d-e2d-561%7C%7C15'

            }
        ]
    a=random.randint(0,len(headers)-1)
    print(a)
    print(headers[int(a)])
    print(headers1[int(a)])
    
    exit(0)
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    print(response.text)
    print(type(response.text))
    exit(0)
    selector = parsel.Selector(response.text)
    city = str(selector.css('.J-current-city::text').get()).strip()  # 城市
    sname = str(selector.css('.shop-name::text').get()).strip()  # 店名
    # n
    print(url)
    print(sname)
    # exit(0)
    j = json.dumps(response.text)
    a = json.loads(j)

    soup = BeautifulSoup(a, 'html.parser')
    company_item = soup.find_all('a', class_="small")
    hot = soup.find_all('a', class_="block-link")
    hot = str(hot)
    hot = BeautifulSoup(hot, 'html.parser')
    hot = hot.find_all('a')
    # print(len(hot))
    # exit(0)
    company_item = str(company_item)
    company_item = BeautifulSoup(company_item, 'html.parser')
    t1 = company_item.find_all('a')
    # print(t1)
    href_list = []
    if (len(hot) > 2):
        hot1 = hot[0].get('href')
        hot2 = hot[1].get('href')
        href_list.append(hot1)
        href_list.append(hot2)
    for t2 in t1:
        t3 = t2.get('href')
        href_list.append(t3)
    cp = 0
    cs = 0
    con = 0  # 项目总数
    # for i in href_list:
    #     if len(i) > 50:
            # sql = "SELECT pid FROM ba_jz_project WHERE time =  '" + \
            #     str(time)+"' and name = '"+name + \
            #     "' and pid = '"+str(id)+"'"  # 检测数据是否存
            # mycursor.execute(sql)
            # myresult = mycursor.fetchall()
            # # myresult = ''
            # if myresult:
            #     # print("已存在")
            #     print(name)
            # else:
            #     # print("不存在")
            #     sql = "insert into ba_jz_project (name, sale,time,price,url,pid) values ('"+name+"','"+str(
            #         saleCount)+"','"+str(time)+"','"+str(price)+"','"+str(urlp)+"','"+str(id)+"')"  # 数据入库
            #     mycursor.execute(sql)
            # mydb.commit()