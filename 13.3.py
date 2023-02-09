# -- coding:UTF-8 --
# 竞争对手数据分析后台系统(数据存入 数据库)
# 店铺项目先入库 后查询对比项目
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
# 项目先入库   对比项目   入库





def filter_string(des_string, re_string=''):
    res = re.compile("[^\\u4e00-\\u9fa5^a-z^A-Z^0-9]")
    return res.sub(re_string, des_string)


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="is_shenzhen90_com"
)



mycursor = mydb.cursor()

# sql = "SELECT `id`,`url`,`name` FROM ba_jzshop  where id =106 order by id "
sql = "SELECT `id`,`url`,`name` FROM ba_jzshop  "
# sql = "SELECT `id`,`url`,`name` FROM ba_jzshop  where id =8  order by id"
# sql = "SELECT `*`, lag (`price`, 1, 0) over (ORDER BY `name`) AS tprice,lag (`sale`, 1, 0) over (ORDER BY `name`) as tsale FROM ba_jz_project WHERE pid = 4 and time>=1666713600 and name in(SELECT name FROM ba_jz_project WHERE time >=1666713600 and pid=4  GROUP BY name HAVING count(name) =2) "
mycursor.execute(sql)
url_list = mycursor.fetchall()

w = datetime.datetime.today().date()
zt = datetime.datetime.today().date() - datetime.timedelta(days=1)  # 格式化时间
date_array = time.strptime(str(w), "%Y-%m-%d")
date_arrayz = time.strptime(str(zt), "%Y-%m-%d")
# print(date_array)
time = int(time.mktime(date_array))  # 今天
ztime = int(time)-24*60*60  # time的昨天
print(time)

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
    return headers


def send_request(url):
    response = requests.get(
        url=f'http://http.tiqu.letecs.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=1&pack=281211&ts=0&ys=0&cs=0&lb=6&sb=,&pb=4&mr=1&regions=&gm=4', headers=request_header())  # 173
    # url=f'http://http.tiqu.letecs.com/getip3?num=6&type=1&pro=&city=0&yys=0&port=1&pack=281211&ts=0&ys=0&cs=0&lb=1&sb=,&pb=4&mr=1&regions=', headers=request_header())
    # url=f'http://http.tiqu.letecs.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=1&pack=252474&ts=0&ys=0&cs=0&lb=6&sb=,&pb=4&mr=1&regions=', headers=request_header())
    # url=f'http://http.tiqu.letecs.com/getip3?num=2&type=1&pro=&city=0&yys=0&port=1&pack=252474&ts=0&ys=0&cs=0&lb=6&sb=,&pb=4&mr=1&regions=', headers=request_header())
    j = response.text
    print(j)
    tr_list = j.split(',')
    print(tr_list)
    for td in tr_list:
        t = td.split(':')
        if t[0] == '{"code"':
            return t[0]
        else:
            try:
                proxy = td.split()[0]  # 115.218.5.5:9000
                ip = test_ip(proxy, url)  # 开始检测获取到的ip是否可以使用
                if proxy == ip:
                    return proxy
            except:
                proxy = ''
                return proxy


def test_ip(proxy, url="https://www.dianping.com/shop/G7Yc9UhIsKP88luu"):
    # 构建代理ip
    proxies = {
        "http": "http://" + str(proxy),
        "https": "http://" + str(proxy)
    }
    try:
        response = requests.get(url=url, headers=request_header(),
                                proxies=proxies, timeout=1)  # 设置timeout，使响应等待1s
        if response.status_code == 200:
            return proxy
    except:
        return (str(proxy)+'请求异常')


proxy = ''

for ur in url_list:

    id = ur[0]
    print(id)
    url = ur[1]

    sql = "SELECT id FROM ba_jz_contend WHERE time =  '" + \
        str(time)+"' and pid = '"+str(id)+"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if myresult:
        print("已存在0跳出本次循环")
        continue  # 跳出本次循环

    # test_ip(proxy,url)
    # proxy = send_request(url)
    # if test_ip(proxy) == proxy:
    if proxy == '':
        proxy = send_request(url)
        if proxy:
            proxies = {
                "http": "http://" + str(proxy),
                "https": "http://" + str(proxy)
            }
        else:
            proxies = ''
        print(proxy)
        # print(0)
    if proxy == '{"code"':
        # print(1)
        print("121今日套餐已用完  115 套餐已过期")
        proxies = ''  # 套餐过期使用本地ip
        # continue
    elif proxy == test_ip(proxy, url):  # 检测ip是否有效
        proxies = {
            "http": "http://" + str(proxy),
            "https": "http://" + str(proxy)
        }
    else:
        while str(proxy)+'请求异常' == test_ip(proxy, url):
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
            if proxy:
                proxies = {
                    "http": "http://" + str(proxy),
                    "https": "http://" + str(proxy)
                }
            else:
                proxies = ''

    print(proxy)
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
            # print(type(logo))

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

            url = urlparse(i)
            paral = parse.parse_qsl(url.query)
            pid = paral[1][1]
            sid = paral[2][1]
            uid = paral[3][1]

            urlp = 'https://www.dianping.com/node/universe-sku/advance/product-detail?pf=dppc&productid=' + \
                str(pid)+'&shopid='+str(sid)+'&shopuuid='+str(uid)

            # # sql = "insert into ba_jz_project (time,url,pid) values ('"+str(time)+"','"+str(urlp)+"','"+str(id)+"') ON DUPLICATE KEY UPDATE time=VALUES('"+str(
            # #     time) + "'),  url=VALUES('" + str(urlp)+"'),  pid= VALUES('"+str(id)+"')"  # 数据没有入库 有则更新  防止重复输入
            # sql = "insert ignore  into ba_jz_project (time,url,pid) values ('"+str(
            #     time)+"','"+str(urlp)+"','"+str(id)+"')"  # 数据入库
            # print(sql)
            # exit(0)
            # mycursor.execute(sql)
            # mydb.commit()

            sql = "SELECT id FROM ba_jz_project WHERE time =  '" + \
                str(time) + "' and url = '"+str(urlp) + \
                "' and pid = '"+str(id)+"'"  # 检测数据是否存
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            # print(myresult)
            if myresult:
                # print("已存在")
                print(id)
            else:
                # print("不存在")
                sql = "insert into ba_jz_project (time,url,pid) values ('"+str(
                    time)+"','"+str(urlp)+"','"+str(id)+"')"  # 数据入库
                mycursor.execute(sql)
            mydb.commit()

    # print(sql)
    # exit(0)

for ur in url_list:

    id = ur[0]
    print(id)
    url = ur[1]

    sql = "SELECT id FROM ba_jz_contend WHERE time =  '" + \
        str(time)+"' and pid = '"+str(id)+"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if myresult:
        print("已存在0跳出本次循环")
        continue  # 跳出本次循环

    if len(city) == 0 or city == 'None':
        print('ct')
        mycursor = mydb.cursor()
        sql = "SELECT city FROM ba_jz_contend WHERE   pid = '" + \
            str(id)+"' limit 0,1"  # 城市
        mycursor.execute(sql)
        city = filter_string(str(mycursor.fetchone()))

    sql = "SELECT id,url FROM ba_jz_project WHERE time =  '" + \
        str(time)+"' and pid = "+str(id)

    mycursor.execute(sql)
    xmdata = mycursor.fetchall()
    cp = 0
    cs = 0
    con = 0  # 项目总数
    # print(xmdata)
    # exit(0)
    for ui in xmdata:

        xid = ui[0]
        i = ui[1]
        url = urlparse(i)
        paral = parse.parse_qsl(url.query)
        pid = paral[1][1]
        sid = paral[2][1]
        uid = paral[3][1]
        url = 'https://mapi.dianping.com/dzbook/prepayproductdetail.json2?platform=pc&channel=dp&clienttype=web&productid=' + \
            str(pid)+'&shopid='+str(sid)+'&shopuuid='+str(uid)
        urlp = 'https://www.dianping.com/node/universe-sku/advance/product-detail?pf=dppc&productid=' + \
            str(pid)+'&shopid='+str(sid)+'&shopuuid='+str(uid)

        response = requests.get(
            url, headers=request_header())
        # print(response)
        j = json.loads(response.text)
        data = j['data']
        if data:
            name = filter_string(data['name'])  # 项目名称
            # data['name'] = filter_string(data['name'])  # 特殊字符过滤
            price = data['price']  # 项目价格
            saleCount = data['saleCount']  # 单个已售数量
            cp += price*saleCount  # 销售总额
            cs += saleCount  # 总销售量
            con = con+1  # 项目总数
            sql = "SELECT pid FROM ba_jz_project WHERE time =  '" + \
                str(time) + "' and url = '"+str(urlp) + "' and name = '"+name + \
                "' and pid = '"+str(id)+"'"  # 检测数据是否存
            # print(sql)
            # exit(0)
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            # myresult = ''
            if myresult:
                # print("已存在")
                print(name)
            else:
                # print("不存在")UPDATE `ba_jz_project` SET `url`='1' WHERE (`id`='1')
                sql = "UPDATE  ba_jz_project  SET  `name`= '"+name+"', `sale`= '"+str(
                    saleCount)+"',  `price`= '"+str(
                    price)+"' WHERE (`id` = '"+str(xid)+"') "  # 今天的项目数据入库
                # print(sql)
                # exit(0)
                mycursor.execute(sql)
            mydb.commit()
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
