# 竞争对手数据分析后台系统(数据存入 数据库)
from cgi import print_arguments
from cmd import IDENTCHARS
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
    # database="is_sz"
)
# 竞争对手数据分析后台系统



mycursor = mydb.cursor()

sql = "SELECT `id`,`url` FROM ba_jzshop order by id"
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
time = int(time.mktime(date_array))#今天
ztime = int(time)-24*60*60#time的昨天
# print(time)
# print(ztime)
# # print(url_list)
# exit(0)
for ur in url_list:
    id= ur[0]
    url= ur[1]
    # print(url)
    # exit(0)
    # shop = url.split('shop/')[1]
    # wjm = str(shop)+str(w)+'.csv'  # 文件名 商店id+时间
    # wjmz = str(shop)+str(zt)+'.csv'  # 文件名 商店id+时间

    # f = open(wjm, 'w', newline='')
    # csv_writer = csv.DictWriter(f, fieldnames=[
    #     '项目名称',
    #     '项目价格',
    #     '销售量',
    # ])
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
    # exit(0)
    selector = parsel.Selector(response.text)
    city = str(selector.css('.J-current-city::text').get()).strip()  # 城市
    sname = str(selector.css('.shop-name::text').get()).strip() # 店名
    # n
    # print(city)
    print(sname)
    # exit(0)
    j = json.dumps(response.text)
    a = json.loads(j)

    soup = BeautifulSoup(a, 'html.parser')
    company_item = soup.find_all('a', class_="small")
    hot = soup.find_all('a', class_="block-link")
    hot =str(hot)
    hot = BeautifulSoup(hot, 'html.parser')
    hot = hot.find_all('a')
    # print(hot)
    # exit(0)
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
                 # https://www.dianping.com/node/universe-sku/advance/product-detail?pf=dppc&productid=758213300&shopid=929234597&shopuuid=HafSlI8fY6WsZ9K2
                #  https://www.dianping.com/node/universe-sku/advance/product-detail?pf=dppc&productid=752326796&shopid=1545823211&shopuuid=laAyczAo9Lm3AkjF
            headers = {
                'Host': 'mapi.dianping.com',
                'Referer': 'https://www.dianping.com/shop/G7Yc9UhIsKP88luu',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                "Cookie": '_lxsdk_cuid=182d2e7a87376-0263598e1d211a-3b3d5203-1fa400-182d2e7a875c8; _lxsdk=182d2e7a87376-0263598e1d211a-3b3d5203-1fa400-182d2e7a875c8; _hc.v=fca25476-1075-20dc-e29a-ed63d2b3c436.1661395775; fspop=test; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1666313445; cy=1; cye=shanghai; s_ViewType=10; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1666336356'
            }
            response = requests.get(url, headers=headers)
            j = json.loads(response.text)
            data = j['data']
            name = filter_string(data['name'])  # 项目名称
            data['name']=filter_string(data['name'])#特殊字符过滤
            price = data['price']  # 项目价格
            saleCount = data['saleCount']  # 单个已售数量
            cp += price*saleCount#销售总额
            cs += saleCount  # 总销售量
            con= con+1#项目总数
            
            
            sql = "SELECT pid FROM ba_jz_project WHERE time =  '"+str(time)+"' and name = '"+name+"' and pid = '"+str(id)+"'"#检测数据是否存
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            # myresult = ''
            if myresult:
                print("已存在")
                print(name)
            else:
                # print("不存在")
                sql = "insert into ba_jz_project (name, sale,time,price,url,pid) values ('"+name+"','"+str(saleCount)+"','"+str(time)+"','"+str(price)+"','"+str(url)+"','"+str(id)+"')"#数据入库
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
    rsale =0
    rtsale =0
    rprice=0
    tprice=0
    shelves=0
    tshelves=0
    
    sql = "SELECT id FROM ba_jz_project WHERE time =  '"+str(ztime)+"' and pid = '"+str(id)+"' limit 0,1"
    mycursor.execute(sql)
    ztdata = mycursor.fetchall()
    if ztdata:#昨天的数据是否存在
        sql="SELECT `name`,`sale`,`price`,`pid` FROM ba_jz_project WHERE time="+str(time)+" and pid="+str(id)+" and name in(SELECT name FROM ba_jz_project WHERE time >="+str(ztime)+" and pid="+str(id)+" GROUP BY name HAVING count(name) =2) ORDER BY `name`"
        mycursor.execute(sql)
        name_list = mycursor.fetchall()# name 相同的数据

        sql="SELECT `name`,`sale`,`price`,`pid` FROM ba_jz_project WHERE time ="+str(ztime)+" and pid="+str(id)+" and name in(SELECT name FROM ba_jz_project WHERE time >="+str(ztime)+" and pid="+str(id)+"  GROUP BY name HAVING count(name) =2) ORDER BY `name`"
        mycursor.execute(sql)
        zname_list = mycursor.fetchall()# name 相同的数据
        
        ne= (set(name_list) - set(zname_list))#去掉完全相同的数据
        en= (set(zname_list) - set(name_list))#去掉完全相同的数据
        # print(len(name_list))
        # print(len(ne))
        # print(len(zname_list))
        # print(len(en))
        for n in ne:
            # print(n)
            for e in en:
                # print(e)
                if(n[0]==e[0]):
                    if(int(n[2])>int(e[2])):#价格不同的数据
                        sql="UPDATE `ba_jz_project` SET `status`='1' WHERE (`name`='"+str(n[0])+"' and `price`='"+str(n[2])+"')"#涨价
                        mycursor.execute(sql)
                        rprice=rprice+1
                        print(n)
                        print(e)
                    elif(int(n[2])<int(e[2])):   
                        sql="UPDATE `ba_jz_project` SET `status`='2' WHERE (`name`='"+str(n[0])+"' and `price`='"+str(n[2])+"')"#降价
                        mycursor.execute(sql)
                        tprice=tprice+1
                        print(n)
                        print(e)
                    if(int(n[1])>int(e[1])):#销售量不同的数据
                        rsale = rsale + (int(n[1])-int(e[1]))  #售货  
                    elif(int(n[1])<int(e[1])):
                        rtsale = rtsale - (int(n[1])-int(e[1])) #退货

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
        ##8.0
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
                    

        sql ="SELECT * FROM ba_jz_project WHERE time>="+str(ztime)+" and  name in( SELECT name FROM ba_jz_project WHERE time>="+str(ztime)+" and pid="+str(id)+" GROUP BY name HAVING count(name) =1) and pid ="+str(id)+" ORDER BY name"
        mycursor.execute(sql)
        dname = mycursor.fetchall()# name 不相同的数据      
        for da in dname:
            print(da)
            if(da[4]==time):
                sql="UPDATE `ba_jz_project` SET `status`='3' WHERE (`id`="+str(da[0])+")"#上架
                rsale = rsale+int(da[2])
                mycursor.execute(sql)
                shelves=shelves+1
            elif(da[4]==ztime):    
                sql="UPDATE `ba_jz_project` SET `status`='4' WHERE (`id`="+str(da[0])+")"#下架
                mycursor.execute(sql)
                tshelves=tshelves+1  
    print(rsale)             
    print(rtsale)             
    print(rprice)             
    print(tprice)             
    print(shelves)             
    print(tshelves)                
    # print(type(rsale))             
    # print(type(rtsale))             
    # print(type(rprice))             
    # print(type(tprice))             
    # print(type(shelves))             
    # print(type(tshelves))                
    # exit(0)     
    sql = "SELECT id FROM ba_jz_contend WHERE time =  '"+str(time)+"' and pid = '"+str(id)+"'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if myresult:
        print("已存在")
    else:
        print("不存在")
        sql = "insert into ba_jz_contend (pid, sale,sales,time,city,rprice,tprice,shelves,tshelves,con) values ('"+str(id)+"','"+str(rsale)+"','"+str(cs)+"','"+str(time)+"','"+city+"','" +str(rprice)+"','"+str(tprice)+"','"+str(shelves)+"','"+str(tshelves)+"','"+str(con)+"')"
        mycursor.execute(sql)
    mydb.commit()