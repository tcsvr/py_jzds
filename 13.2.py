# -- coding:UTF-8 --
# 竞争对手数据分析后台系统(数据存入 数据库)
from cgi import print_arguments
from cmd import IDENTCHARS
from re import T
import requests
import parsel
# import csv
import os
import time
import datetime
from bs4 import BeautifulSoup
from urllib import parse
from urllib.parse import urlparse
# from lxml import etree
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

sql = "SELECT `id`,`url`,`name` FROM ba_jzshop  order by id "
# sql = "SELECT `id`,`url`,`name` FROM ba_jzshop  where id =8  order by id"
# sql = "SELECT `*`, lag (`price`, 1, 0) over (ORDER BY `name`) AS tprice,lag (`sale`, 1, 0) over (ORDER BY `name`) as tsale FROM ba_jz_project WHERE pid = 4 and time>=1666713600 and name in(SELECT name FROM ba_jz_project WHERE time >=1666713600 and pid=4  GROUP BY name HAVING count(name) =2) "
mycursor.execute(sql)
url_list = mycursor.fetchall()
# for ur in url_list:
#     print(ur)
# exit(0)
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
date_arrayz = time.strptime(str(zt), "%Y-%m-%d")
# print(date_array)
# print(date_arrayz)
time = int(time.mktime(date_array))  # 今天
ztime = int(time)-24*60*60  # time的昨天

print(time)
# print(ztime)
# print(url_list)
# exit(0)
# import time
# 睡眠时间
# def sleeptime(s):
#     # 时间间隔time秒
#     print("休息",end="")
#     for i in range(s):
#         print(type(s))
#         time.sleep(1)
#         print("第"+str(i+1)+"秒 ",end="")
# # print(time)
# exit(0)

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
        url=f'http://http.tiqu.letecs.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=1&pack=252474&ts=0&ys=0&cs=0&lb=6&sb=,&pb=4&mr=1&regions=', headers=request_header())
    # url=f'http://http.tiqu.letecs.com/getip3?num=2&type=1&pro=&city=0&yys=0&port=1&pack=252474&ts=0&ys=0&cs=0&lb=6&sb=,&pb=4&mr=1&regions=', headers=request_header())
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


def test_ip(proxy, url="http://www.shenzhen91.com/"):
    # 构建代理ip
    proxies = {
        "http": "http://" + str(proxy),
        "https": "http://" + str(proxy)
    }
    try:
        response = requests.get(url=url, headers=request_header(),
                                proxies=proxies, timeout=1)  # 设置timeout，使响应等待1s
        if response.status_code == 200:
            # print(proxy)
            return proxy

    except:
        # if str(proxy).split(':')[1] == '121' or str(proxy).split(':')[1] == '115':
        #     return proxy  # 今日套餐已用完
        # else:
        return str(proxy)+'请求异常'


# print(url_list[0][1])
# proxy = send_request(url_list[0][1])
# exit(0)
proxy = ''

for ur in url_list:
    id = ur[0]
    url = ur[1]

    sql = "SELECT id FROM ba_jz_contend WHERE time =  '" + \
        str(time)+"' and pid = '"+str(id)+"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if myresult:
        print(id)
        print("已存在0跳出本次循环")
        continue  # 跳出本次循环

    # test_ip(proxy,url)
    # proxy = send_request(url)
    # if test_ip(proxy) == proxy:
    if proxy == '':
        proxy = send_request(url)
    if proxy == '{"code":121' or proxy == '{"code":115':
        print("121今日套餐已用完  115 套餐已过期")
        proxies = ''  # 套餐过期使用本地ip
        # continue
    elif test_ip(proxy, url) == proxy:  # 检测ip是否有效
        proxies = {
            "http": "http://" + str(proxy),
            "https": "http://" + str(proxy)
        }
    else:
        while test_ip(proxy, url) != str(proxy)+'请求异常':
            # 时间间隔time秒
            import time
            def sleeptime(s):
                print("休息", end="")
                for i in range(s):
                    time.sleep(1)
                    print("第"+str(i+1)+"秒 ", end="")
            stime = random.randint(1, 2)
            sleeptime(stime)
            time = int(time.mktime(date_array))  # 今天(命名出现bug 重新获取时间)
            proxy = send_request(url)
            proxies = {
                "http": "http://" + str(proxy),
                "https": "http://" + str(proxy)
            }
    # print(proxy)
    # if (type(send_request(url)) == 'NoneType'):
    #     print(11)
    # exit(0)
    # print(1)

    # exit(0)221.203.6.46:3935 请求异常
    response = requests.get(url, headers=request_header(), proxies=proxies)
    response.encoding = "utf-8"
    # print(response.text)
    print(type(response.text))
    selector = parsel.Selector(response.text)
    # selector=''
    logo = str(selector.css('.logo::text').get()).strip()  # 出现验证问题
    while logo == '验证中心':
        # 睡眠时间
        import time

        def sleeptime(s):
            # 时间间隔time秒
            print("休息", end="")
            for i in range(s):
                time.sleep(1)
                print("第"+str(i+1)+"秒 ", end="")
        stime = random.randint(3, 4)
        sleeptime(stime)
        time = int(time.mktime(date_array))  # 今天(命名出现bug 重新获取时间)

        if test_ip(proxy, url) == proxy:
            response = requests.get(
                url, headers=request_header(), proxies=proxies)
            response.encoding = "utf-8"
            # print(response.text)
            print(logo)
            selector = parsel.Selector(response.text)
            # selector=''
            logo = str(selector.css('.logo::text').get()).strip()  # 城市
            print(type(logo))

        else:
            break

    city = str(selector.css('.J-current-city::text').get()).strip()  # 城市
    # print('logo1'+str(logo))
    # print('dizhi1'+str(city))
    # exit(0)
    city = str(selector.css('.J-current-city::text').get()).strip()  # 城市
    if len(city) == 0 or city == 'None':
        mycursor = mydb.cursor()
        sql = "SELECT city FROM ba_jz_contend WHERE   pid = '" + \
            str(id)+"' limit 0,1"  # 城市
        mycursor.execute(sql)
        city = filter_string(str(mycursor.fetchone()))

    sname = str(selector.css('.shop-name::text').get()).strip()  # 店名
    if len(sname) == 0 or sname == 'None':
        sname = ur[2]
    # n
    print(url)
    print(city)
    print(sname)
    # print('sss')
    # print(len(city))
    # print(len(sname))
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
    if len(href_list) == 0 or href_list == 'None':
        sql = "SELECT id,url FROM ba_jz_project WHERE time =  '" + \
            str(ztime)+"' and pid = '"+str(id)+"'"  # 检测数据是否存
        mycursor.execute(sql)
        href_lis = mycursor.fetchall()
        # print(href_lis)
        if href_lis:
            for i in href_lis:
                href_list.append(i[1])
        # print('sql1')
    for i in href_list:
        if len(i) > 50:

            # import time
            # # 睡眠时间
            # def sleeptime(s):
            #     # 时间间隔time秒
            #     print("休息", end="")
            #     for i in range(s):
            #         time.sleep(1)
            #         print("第"+str(i+1)+"秒 ", end="")
            # stime = random.randint(1,3)
            # sleeptime(stime)
            # time = int(time.mktime(date_array)) # 今天(命名出现bug 重新获取时间)

            url = urlparse(i)
            paral = parse.parse_qsl(url.query)
            pid = paral[1][1]
            sid = paral[2][1]
            uid = paral[3][1]
            url = 'https://mapi.dianping.com/dzbook/prepayproductdetail.json2?platform=pc&channel=dp&clienttype=web&productid=' + \
                str(pid)+'&shopid='+str(sid)+'&shopuuid='+str(uid)
            urlp = 'https://www.dianping.com/node/universe-sku/advance/product-detail?pf=dppc&productid=' + \
                str(pid)+'&shopid='+str(sid)+'&shopuuid='+str(uid)
            #  https://www.dianping.com/node/universe-sku/advance/product-detail?pf=dppc&productid=752326796&shopid=1545823211&shopuuid=laAyczAo9Lm3AkjF
            # headers = {
            #     'Host': 'mapi.dianping.com',
            #     'Referer': urlp,
            #     'User-Agent':UserAgent().firefox,
            #     # 'User-Agent':UserAgent().Chrome,
            #     # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            #     "Cookie": 'cy=1; cityid=1; cye=shanghai; _lxsdk_cuid=18407d265b220-02df1e3ca332668-4076032e-1fa400-18407d265b4c8; _lxsdk=18407d265b220-02df1e3ca332668-4076032e-1fa400-18407d265b4c8; _hc.v=b7d2b53a-4bba-c0d1-8e4c-e3895822e059.1666578540; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1666578540,1667871521; _lxsdk_s=18454e3b505-c63-096-5a7%7C%7C1; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1667871521'
            # }

            # print(headers[int(ha)])d
            # if proxy == '{"code":121' or proxy == '{"code":115':
            #     print("121今日套餐已用完  115 套餐已过期")
            #     proxies = ''  # 套餐过期使用本地ip
            #     # continue
            # elif test_ip(proxy, url) == proxy:  # 检测ip是否有效
            #     proxies = {
            #         "http": "http://" + str(proxy),
            #         "https": "http://" + str(proxy)
            #     }
            # else:
            #     while test_ip(proxy, url) != proxy:
            #         proxy = send_request(url)
            #         proxies = {
            #             "http": "http://" + str(proxy),
            #             "https": "http://" + str(proxy)
            #         }

            response = requests.get(
                url, headers=request_header())
            # print(response)
            j = json.loads(response.text)
            data = j['data']
            name = filter_string(data['name'])  # 项目名称
            data['name'] = filter_string(data['name'])  # 特殊字符过滤
            price = data['price']  # 项目价格
            saleCount = data['saleCount']  # 单个已售数量
            cp += price*saleCount  # 销售总额
            cs += saleCount  # 总销售量
            con = con+1  # 项目总数

            sql = "SELECT pid FROM ba_jz_project WHERE time =  '" + \
                str(time)+"' and name = '"+name + \
                "' and pid = '"+str(id)+"'"  # 检测数据是否存
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            # myresult = ''
            if myresult:
                # print("已存在")
                print(name)
            else:
                # print("不存在")
                sql = "insert into ba_jz_project (name, sale,time,price,url,pid) values ('"+name+"','"+str(
                    saleCount)+"','"+str(time)+"','"+str(price)+"','"+str(urlp)+"','"+str(id)+"')"  # 数据入库
                mycursor.execute(sql)
            mydb.commit()

            # print(name)
            # print(price)
            # print(saleCount)
    #         dit = {
    #             '项目名称': data['name'],
    #             '项目价格': data['price'],
    #             '销售量': data['saleCount'],
    #         }
    #         csv_writer.writerow(dit)
    # f.close()# 影响后面函数 compa
    print(cs)  # 总销售量
    # exit(0)
    rsale = 0
    rtsale = 0
    rprice = 0
    tprice = 0
    shelves = 0
    tshelves = 0

    sql = "SELECT id FROM ba_jz_project WHERE time =  '" + \
        str(ztime)+"' and pid = '"+str(id)+"' limit 0,1"
    mycursor.execute(sql)
    ztdata = mycursor.fetchall()
    if ztdata:  # 昨天的数据是否存在
        sql = "SELECT `name`,`sale`,`price`,`pid` FROM ba_jz_project WHERE time="+str(time)+" and pid="+str(
            id)+" and name in(SELECT name FROM ba_jz_project WHERE time >="+str(ztime)+" and pid="+str(id)+" GROUP BY name HAVING count(name) =2) ORDER BY `name`"
        mycursor.execute(sql)
        name_list = mycursor.fetchall()  # name 相同的数据

        sql = "SELECT `name`,`sale`,`price`,`pid` FROM ba_jz_project WHERE time ="+str(ztime)+" and pid="+str(
            id)+" and name in(SELECT name FROM ba_jz_project WHERE time >="+str(ztime)+" and pid="+str(id)+"  GROUP BY name HAVING count(name) =2) ORDER BY `name`"
        mycursor.execute(sql)
        zname_list = mycursor.fetchall()  # name 相同的数据

        ne = (set(name_list) - set(zname_list))  # 去掉完全相同的数据
        en = (set(zname_list) - set(name_list))  # 去掉完全相同的数据
        # print(len(name_list))
        # print(len(ne))
        # print(len(zname_list))
        # print(len(en))
        for n in ne:
            # print(n)
            for e in en:
                # print(e)
                if (n[0] == e[0]):
                    if (int(n[2]) > int(e[2])):  # 价格不同的数据
                        sql = "UPDATE `ba_jz_project` SET `status`='1' WHERE (`name`='"+str(
                            n[0])+"' and `price`='"+str(n[2])+"')"  # 涨价
                        mycursor.execute(sql)
                        rprice = rprice+1
                        print(n)
                        print(e)
                    elif (int(n[2]) < int(e[2])):
                        sql = "UPDATE `ba_jz_project` SET `status`='2' WHERE (`name`='"+str(
                            n[0])+"' and `price`='"+str(n[2])+"')"  # 降价
                        mycursor.execute(sql)
                        tprice = tprice+1
                        print(n)
                        print(e)
                    if (int(n[1]) > int(e[1])):  # 销售量不同的数据
                        rsale = rsale + (int(n[1])-int(e[1]))  # 售货
                    elif (int(n[1]) < int(e[1])):
                        rtsale = rtsale - (int(n[1])-int(e[1]))  # 退货

        # for na in name_list:
        #     # print(na)
        #     for zna in zname_list:
        #         # print(zna)
        #         if(na[1]==zna[1]):
        #             if(int(na[3])>int(zna[3])):
        #                 sql="UPDATE `ba_jz_project` SET `status`='1' WHERE (`id`="+str(na[0])+")"#涨价
        #                 mycursor.execute(sql)
        #                 rprice=rprice+1
        #                 print(na)
        #                 print(zna)
        #             elif(int(na[3])<int(zna[3])):
        #                 sql="UPDATE `ba_jz_project` SET `status`='2' WHERE (`id`="+str(na[0])+")"#降价
        #                 mycursor.execute(sql)
        #                 tprice=tprice+1
        #                 print(na)
        #                 print(zna)
        #             if(int(na[2])>int(zna[2])):
        #                 rsale =rsale+ (int(na[2])-int(zna[2]))  #售货
        #             elif(int(na[2])<int(zna[2])):
        #                 rtsale = rtsale - (int(na[2])-int(zna[2])) #退货
        # 8.0
        # sql = "SELECT `*`, lag (`price`, 1, 0) over (ORDER BY `name`) AS tprice,lag (`sale`, 1, 0) over (ORDER BY `name`) as tsale FROM ba_jz_project WHERE pid = "+str(id)+" and time>="+str(ztime)+" and name in(SELECT name FROM ba_jz_project WHERE time >="+str(ztime)+" and pid="+str(id)+"  GROUP BY name HAVING count(name) =2) "
        # mycursor.execute(sql)
        # url_list = mycursor.fetchall()# name 相同的数据
        # for ur in url_list:
        #     # print (ur)
        #     if(ur[4]==time):
        #         if(int(ur[3])>int(ur[7])):
        #             sql="UPDATE `ba_jz_project` SET `status`='1' WHERE (`id`="+str(ur[0])+")"#涨价
        #             mycursor.execute(sql)
        #             rprice=+1
        #             print(ur)
        #         elif(int(ur[3])<int(ur[7])):
        #             sql="UPDATE `ba_jz_project` SET `status`='2' WHERE (`id`="+str(ur[0])+")"#降价
        #             mycursor.execute(sql)
        #             tprice=+1
        #             print(ur)
        #         if(int(ur[2])>int(ur[8])):
        #             rsale = rsale + (int(ur[2])-int(ur[8]))
        #         elif(int(ur[2])<int(ur[8])):
        #             rtsale = rtsale - (int(ur[2])-int(ur[8]))
        sql = "SELECT id FROM ba_jz_project WHERE time =  '" + \
            str(time)+"' and pid = '"+str(id)+"' limit 0,1"
        mycursor.execute(sql)
        jtdata = mycursor.fetchall()
        if jtdata:  # 今天的数据是否存在
            sql = "SELECT * FROM ba_jz_project WHERE time>="+str(ztime)+" and  name in( SELECT name FROM ba_jz_project WHERE time>="+str(
                ztime)+" and pid="+str(id)+" GROUP BY name HAVING count(name) =1) and pid ="+str(id)+" ORDER BY name"
            mycursor.execute(sql)
            dname = mycursor.fetchall()  # name 不相同的数据
            for da in dname:
                print(da)
                if (da[4] == time):
                    # 上架
                    sql = "UPDATE `ba_jz_project` SET `status`='3' WHERE (`id`="+str(
                        da[0])+")"
                    rsale = rsale+int(da[2])
                    mycursor.execute(sql)
                    shelves = shelves+1
                elif (da[4] == ztime):
                    # 下架
                    sql = "UPDATE `ba_jz_project` SET `status`='4' WHERE (`id`="+str(
                        da[0])+")"
                    mycursor.execute(sql)
                    tshelves = tshelves+1
    print(rsale)
    print(rtsale)
    print(rprice)
    print(tprice)
    print(shelves)
    print(tshelves)
    print(con)
    # print(type(rsale))
    # print(type(rtsale))
    # print(type(rprice))
    # print(type(tprice))
    # print(type(shelves))
    # print(type(tshelves))
    # exit(0)
    sql = "SELECT id FROM ba_jz_contend WHERE time =  '" + \
        str(time)+"' and pid = '"+str(id)+"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if myresult:
        print("已存在contend")
    else:
        print("不存在contend")
        if con != 0:  # 判断是否获取到数据
            sql = "insert into ba_jz_contend (pid, sale,sales,time,city,rprice,tprice,shelves,tshelves,con) values ('"+str(id)+"','"+str(rsale)+"','"+str(
                cs)+"','"+str(time)+"','"+city+"','" + str(rprice)+"','"+str(tprice)+"','"+str(shelves)+"','"+str(tshelves)+"','"+str(con)+"')"
            mycursor.execute(sql)
        # else:#如果没有获取到数据 延时一段时间后再次爬取
        #     print('延时执行')
            # import time
            # # 睡眠时间
            # def sleeptime(s):
            #     # 时间间隔time秒
            #     print("休息",end="")
            #     for i in range(s):
            #         time.sleep(1)
            #         print("第"+str(i+1)+"秒 ",end="")
            # sleeptime(300)
            # time = int(time.mktime(date_array))#今天(命名出现bug 重新获取时间)
    mydb.commit()
