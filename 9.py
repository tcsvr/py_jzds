# 竞争对手数据分析后台系统
from cgi import print_arguments
from re import T
import requests
import parsel
import csv
import re
import time
import datetime
from bs4 import BeautifulSoup
from urllib import parse
from urllib.parse import urlparse
from lxml import etree
from scrapy import Selector
import json
import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="is_shenzhen90_com"
)
# 竞争对手数据分析后台系统



mycursor = mydb.cursor()

# f =open('1023.csv', 'w', newline='')
# csv_writer = csv.DictWriter(f, fieldnames=[
#         # '项目编号',
#         '项目名称',
#         '项目价格',
#         '销售量',
#         # '总价',
#         # '平台',
#         # '环境',
#         # '服务',
#         # '地址',
#         # '电话',
#         # '详情页',
# ])
# # csv_writer.writeheader()


# for x in range(2,108):
url = 'https://www.dianping.com/shop/G7Yc9UhIsKP88luu'

# print(url)
# shop = re.findall("shop/(.*?)\?",url)[0]
shop = url.split('shop/')[1]
w = datetime.datetime.today().date()
zt = datetime.datetime.today().date() - datetime.timedelta(days=1)  # 格式化时间

# 1、时间字符串转成时间数组形式
date_array = time.strptime(str(w), "%Y-%m-%d")
# 2、查看时间数组数据
# print("时间数组：", date_array)
# 3、mktime时间数组转成时间戳
time = int(time.mktime(date_array))

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
# print(selector)
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
# print(hot[0].get('href'))
company_item = str(company_item)
company_item = BeautifulSoup(company_item, 'html.parser')
# print(type(company_item))
# print(type(soup))
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
# print(href_list)
# exit(0)
for i in href_list:
    if len(i) > 50:
        # print(i)
        # url =urlparse('https://g.dianping.com/fuse/HktMNFLCM?pf=dppc&productid=671998827&shopid=131360635&shopuuid=G7Yc9UhIsKP88luu')
        url = urlparse(i)
        paral = parse.parse_qsl(url.query)
        # print(paral)
        pid = paral[1][1]
        sid = paral[2][1]
        uid = paral[3][1]
        # sid=url[73:82]
        # uid = []
        # url ='https://g.dianping.com/fuse/HktMNFLCM?pf=dppc&productid=671998827&shopid=131360635&shopuuid=G7Yc9UhIsKP88luu'
        # url ='https://g.dianping.com/fuse/HktMNFLCM?pf=dppc&productid=627303388&shopid=18048888&shopuuid=l9pH11K90f0a9dDA'
        # print(pid)
        # print(sid)
        # print(uid)
        # print(type(url))
        # url ='https://mapi.dianping.com/dzbook/prepayproductdetail.json2?platform=pc&channel=dp&clienttype=web&productid=671998827&shopid=131360635&shopuuid=G7Yc9UhIsKP88luu&cityid=7'
        # url ='https://mapi.dianping.com/dzbook/prepayproductdetail.json2?platform=pc&channel=dp&clienttype=web&productid=627303388&shopid=18048888&shopuuid=l9pH11K90f0a9dDA&cityid=7'
        url = 'https://mapi.dianping.com/dzbook/prepayproductdetail.json2?platform=pc&channel=dp&clienttype=web&productid=' + \
            str(pid)+'&shopid='+str(sid)+'&shopuuid='+str(uid)+'&cityid=7'

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
        price = data['price']  # 项目价格
        saleCount = data['saleCount']  # 已售数量
        cp += price*saleCount
        cs += saleCount  # 总销售量
        # cp+=price*saleCount
        con= con+1#项目总数
        print(name)
        print(price)
        print(saleCount)
        # print(cp)

        dit = {
            '项目名称': data['name'],
            '项目价格': data['price'],
            '销售量': data['saleCount'],
        }
        csv_writer.writerow(dit)
f.close()#十分重要 影响后面函数 compa    
print(cp)  # 销售总额

# import time
# # 睡眠时间
# def sleeptime(s):
#     # 时间间隔time秒
#     print("休息",end="")
#     for i in range(s):
#         time.sleep(1)
#         print("第"+str(i+1)+"秒 ",end="")
# sleeptime(60)

def compa(x, y):
    with open(x, "r", encoding="ANSI") as f:
        red = csv.reader(f)
        print(red)
        count = 0
        up = 0
        dw = 0
        seal = 0
        sea = 0
        xz = 0
        js = 0
        res = []
        dt = []
       
        # i = int()
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


# if __name__ == "__main__":

datas = compa(wjm, wjmz)
print(datas)
# exit(0)
sql = "SELECT * FROM ba_contend WHERE time =  '"+str(time)+"' and name = '"+sname+"'"
mycursor.execute(sql)
myresult = mycursor.fetchall()
if myresult:
    print("已存在")
else:
    print("不存在")
    sql = "insert into ba_contend (name, sale,sales,time,city,rprice,tprice,shelves,tshelves,con) values ('"+sname+"','"+str(datas[4])+"','"+str(cs)+"','"+str(time)+"','"+city+"','" +str(datas[0])+"','"+str(datas[1])+"','"+str(datas[2])+"','"+str(datas[3])+"','"+str(con)+"')"
    mycursor.execute(sql)
mydb.commit()
# sql = "insert into ba_content (comments, platform,commentime,userid,username,admin_id) values ('"+count+"','"+platform+"','"+commentTime+"','"+str(userId)+"','"+userName+"','25')"
# mycursor.execute(sql)
# mydb.commit()

# https://mapi.dianping.com/dzbook/prepayproductdetail.json2?platform=pc&channel=dp&clienttype=web&productid=671998827&shopid=131360635&shopuuid=G7Yc9UhIsKP88luu&cityid=7

# print((a))
# title = selector.css('.price::text').get()  # 店名
# print(title)
# print(response.text)
# print(response.text)
# count = selector.css('#sales::text').extract()
# print(count)
# j = json.loads(count[0])
# print(j)
# print(j['data']['commentDTOList'])
# con = (j['data']['commentDTOList'])#wap端评论
# con = (j['comments'])#pc端评论
# print(con)

# for i in con:
#     # count = i['comment'].replace('\U0001f44d', '')  # 评论
#     count = re.sub("[^，。\\u4e00-\\u9fa5^a-z^A-Z^0-9^%&',.;=?$\x22]", "", i['comment'])   # 评论
#     count = count.replace('劲松','')  # 评论过滤
#     count = count.replace("'",'"')  # 评论过滤
#     commentTime = i['commentTime']  #评论时间
#     userId = i['userId']  # 用户id
#     print(x)
#     print('===')
#     print(str(i['userId']))
#     userName = i['userName']  # 用户名
#     platform = '美团_劲松口腔医院（外企院）'  # 平台
#     star=i['star']#评分
#     print(star)
#     if star >=30:#3颗星以上数据
# 数据库插入
# if count != '' and len(count) >16:
#     sql = "SELECT * FROM ba_review_system WHERE platform = '"+platform+"' and commentime = '"+commentTime+"' and userid = '"+str(userId)+"' and username = '"+userName+"'"
#     mycursor.execute(sql)
#     myresult = mycursor.fetchall()
#     if myresult:
#         print("已存在")
#     else:
#         print("不存在")#  admin_id  妇科 = 16 ; 产科=22;  美容=20; 体检=18; 口腔=25;眼科=28；
#         sql = "insert into ba_review_system (comments, platform,commentime,userid,username,admin_id) values ('"+count+"','"+platform+"','"+commentTime+"','"+str(userId)+"','"+userName+"','25')"
#         mycursor.execute(sql)
#     mydb.commit()

#     Price = count[i]['comment'] # 人均消费
#     item_list = selector_1.css('#comment_score .item::text').getall()  # 评价
#     taste = item_list[0].split(': ')[-1]  # 口味评分
#     environment = item_list[1].split(': ')[-1]  # 环境评分
#     service = item_list[-1].split(': ')[-1]  # 服务评分
#     address = selector_1.css('#address::text').get()  # 地址
#     tel = selector_1.css('.tel ::text').getall()[-1]  # 电话

# dit = {
#     '项目名称': count,
#     '项目价格': commentTime,
#     '销售量': userId,
#     '总价': userName,
# }
# csv_writer.writerow(dit)
