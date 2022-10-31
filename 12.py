# 竞争对手数据分析后台系统（数据存入 csv文件）
from cgi import print_arguments
from re import T
import requests
import parsel
import csv
import os
import time
import datetime
from bs4 import BeautifulSoup
from urllib import parse
from urllib.parse import urlparse
from lxml import etree
from scrapy import Selector
import json
import mysql.connector

import re
# 通过re过滤除中英文及数字以外的其他字符
def filter_string(des_string, re_string=''):
    res = re.compile("[^\\u4e00-\\u9fa5^a-z^A-Z^0-9]")
    return res.sub(re_string, des_string)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="is_shenzhen90_com"
)
# 竞争对手数据分析后台系统

# mydb = mysql.connector.connect(#线上服务器数据库
#   host="rdsrvrsep06wyx67yl78po.mysql.rds.aliyuncs.com",
#   user="ls_shenzhen91_co",
#   passwd="Stc64nb4hxcrdGtm",
#   database="ls_shenzhen91_co"
# )

mycursor = mydb.cursor()

sql = "SELECT id ,url FROM ba_shop "
mycursor.execute(sql)
url_list = mycursor.fetchall()
# print(url_list)
# for ur in url_list:
#     id= ur[0]
#     url= ur[1]
#     print(url)

# exit(0)

# url_list=[
#     'https://www.dianping.com/shop/G7Yc9UhIsKP88luu',
#     'https://www.dianping.com/shop/l9pH11K90f0a9dDA',
#     'https://www.dianping.com/shop/l5kzDxpJs4vd1LGQ',
#     'https://www.dianping.com/shop/H3jIjng6tblpk41Y',
# ]
w = datetime.datetime.today().date()
zt = datetime.datetime.today().date() - datetime.timedelta(days=1)  # 格式化时间
date_array = time.strptime(str(w), "%Y-%m-%d")
time = int(time.mktime(date_array))
for ur in url_list:
    id= ur[0]
    url= ur[1]
    shop = url.split('shop/')[1]
    wjm = str(shop)+str(w)+'.csv'  # 文件名 商店id+时间
    wjmz = str(shop)+str(zt)+'.csv'  # 文件名 商店id+时间

    f = open(wjm, 'w', newline='')
    csv_writer = csv.DictWriter(f, fieldnames=[
        '项目名称',
        '项目价格',
        '销售量',
    ])
    # csv_writer.writeheader()

    headers = {
        'Host': 'www.dianping.com',
        'Referer': 'https://www.dianping.com/shop/G7Yc9UhIsKP88luu',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        "Cookie": '_lxsdk_cuid=182d2e7a87376-0263598e1d211a-3b3d5203-1fa400-182d2e7a875c8; _lxsdk=182d2e7a87376-0263598e1d211a-3b3d5203-1fa400-182d2e7a875c8; _hc.v=fca25476-1075-20dc-e29a-ed63d2b3c436.1661395775; fspop=test; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1666313445; cy=1; cye=shanghai; s_ViewType=10; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1666318032; _lxsdk_s=183f85aba51-441-c20-3e7%7C%7C1'
    }

    response = requests.get(url, headers=headers)
    # print(response.text)
    print(type(response.text))
    selector = parsel.Selector(response.text)
    city = selector.css('.J-current-city::text').get().strip()  # 城市
    sname = selector.css('.shop-name::text').get().strip()  # 店名
    # n
    print(sname)
    j = json.dumps(response.text)
    a = json.loads(j)

    soup = BeautifulSoup(a, 'html.parser')
    company_item = soup.find_all('a', class_="small")
    hot = soup.find_all('a', class_="block-link")
    hot =str(hot)
    hot = BeautifulSoup(hot, 'html.parser')
    hot = hot.find_all('a')
    hot1=hot[0].get('href')
    hot2=hot[1].get('href')
    company_item = str(company_item)
    company_item = BeautifulSoup(company_item, 'html.parser')
    t1 = company_item.find_all('a')
    # print(t1)
    href_list = []
    href_list.append(hot1)
    href_list.append(hot2)
    for t2 in t1:
        t3 = t2.get('href')
        href_list.append(t3)
    cp = 0
    cs = 0
    con = 0  # 项目总数
    for i in href_list:
        if len(i) > 50:
            url = urlparse(i)
            paral = parse.parse_qsl(url.query)
            pid = paral[1][1]
            sid = paral[2][1]
            uid = paral[3][1]
            url = 'https://mapi.dianping.com/dzbook/prepayproductdetail.json2?platform=pc&channel=dp&clienttype=web&productid='+str(pid)+'&shopid='+str(sid)+'&shopuuid='+str(uid)+'&cityid=7'
            headers = {
                'Host': 'mapi.dianping.com',
                'Referer': 'https://www.dianping.com/shop/G7Yc9UhIsKP88luu',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                "Cookie": '_lxsdk_cuid=182d2e7a87376-0263598e1d211a-3b3d5203-1fa400-182d2e7a875c8; _lxsdk=182d2e7a87376-0263598e1d211a-3b3d5203-1fa400-182d2e7a875c8; _hc.v=fca25476-1075-20dc-e29a-ed63d2b3c436.1661395775; fspop=test; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1666313445; cy=1; cye=shanghai; s_ViewType=10; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1666336356'
            }
            response = requests.get(url, headers=headers)
            j = json.loads(response.text)
            data = j['data']
            name = data['name']  # 项目名称
            data['name']=filter_string(data['name'])#特殊字符过滤
            price = data['price']  # 项目价格
            saleCount = data['saleCount']  # 单个已售数量
            cp += price*saleCount#销售总额
            cs += saleCount  # 总销售量
            con= con+1#项目总数
            # print(name)
            # print(price)
            # print(saleCount)
            dit = {
                '项目名称': data['name'],
                '项目价格': data['price'],
                '销售量': data['saleCount'],
            }
            csv_writer.writerow(dit)
    f.close()# 影响后面函数 compa    
    print(cs)  # 总销售量

    def compa(x, y):
        tf=os.path.exists(y)
        if tf!=True:
            y=x
            dt=[0,0,0,0,]
            return dt 
        with open(x, "r", encoding="ANSI") as f:
            red = csv.reader(f)
            # print(red)
            count = 0
            up = 0
            dw = 0
            seal = 0
            sea = 0
            xz = 0
            js = 0
            res = []
            dt = []
            for r in red:
                res.append(r)
                flag = 0  # 判断是否出现不同
                fg = 0  # 判断是否新增
                with open(y, encoding="ANSI") as n:
                    dat = csv.reader(n)
                    da = []
                    for d in dat:
                        da.append(d)
                        if r == d:
                            count = count+1
                            flag = 1
                            break
                    if flag == 0:
                        for j in da:
                            if r[0] == j[0]:
                                price = int(float(r[1]))-int(float(j[1]))
                                if price > 0:
                                    up = up+1
                                elif price < 0:
                                    dw = dw+1
                                se = int(r[2])-int(j[2])
                                if se >= 0:
                                    seal = seal + se
                                else:
                                    sea = sea - se
                                fg = 1
                        if fg == 0:  # 项目新增
                            print(r)
                            xz = xz+1
                            seal = seal + int(r[2])
            for j in da:  # 项目减少判断
                fla = 0
                fl = 0
                for r in res:
                    if r == j:
                        fla = 1
                        break
                if fla == 0:
                    # print(j)
                    for r in res:
                        if j[0] == r[0]:
                            fl = 1
                            break
                    if fl == 0:
                        print(j)
                        js = js+1
            dt.append(up)
            dt.append(dw)
            dt.append(xz)
            dt.append(js)
            dt.append(seal)
            print("相同的数据总共有：", count)
            print("涨价的数据总共有：", up)
            print("降价的数据总共有：", dw)
            print("项目新增上架：", xz)
            print("项目减少下架：", js)
            print("日售：", seal)
            print("退货：", sea)
            return dt
    datas = compa(wjm, wjmz)
    print(datas)
    # exit(0)
    sql = "SELECT id FROM ba_contend WHERE time =  '"+str(time)+"' and pid = '"+str(id)+"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if myresult:
        print("已存在")
    else:
        print("不存在")
        sql = "insert into ba_contend (pid, sale,sales,time,city,rprice,tprice,shelves,tshelves,con) values ('"+str(id)+"','"+str(datas[4])+"','"+str(cs)+"','"+str(time)+"','"+city+"','" +str(datas[0])+"','"+str(datas[1])+"','"+str(datas[2])+"','"+str(datas[3])+"','"+str(con)+"')"
        mycursor.execute(sql)
    mydb.commit()