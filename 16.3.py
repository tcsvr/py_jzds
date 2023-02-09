from cgi import print_arguments
from cmd import IDENTCHARS
from re import T
import requests
from urllib import parse
from urllib.parse import urlparse
import mysql.connector
from fake_useragent import UserAgent

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
        # url=f'http://http.tiqu.letecs.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=1&pack=281208&ts=0&ys=0&cs=0&lb=1&sb=,&pb=4&mr=1&regions=', headers=request_header())
    # url=f'http://http.tiqu.letecs.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=,&pb=4&mr=1&regions=', headers=request_header())
    # url=f'http://http.tiqu.letecs.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=1&pack=252474&ts=0&ys=0&cs=0&lb=6&sb=,&pb=4&mr=1&regions=', headers=request_header())
    url=f'http://http.tiqu.letecs.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=1&pack=281211&ts=0&ys=0&cs=0&lb=6&sb=,&pb=4&mr=1&regions=&gm=4', headers=request_header())
    j = response.text
    tr_list = j.split(',')
    # print(tr_list)
    for td in tr_list:
        t= td.split(':')
        if t[0] == '{"code"':
            return t[0]
        else:
            proxy = td.split()[0]  # 115.218.5.5:9000
            ip = test_ip(proxy, url)  # 开始检测获取到的ip是否可以使用
            if proxy == ip:
                return proxy
def send_request1(url):
    response = requests.get(
        url=f'http://http.tiqu.letecs.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=1&pack=281208&ts=0&ys=0&cs=0&lb=1&sb=,&pb=4&mr=1&regions=', headers=request_header())
        # url=f'http://http.tiqu.letecs.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=1&pack=281211&ts=0&ys=0&cs=0&lb=6&sb=,&pb=4&mr=1&regions=&gm=4', headers=request_header())
    # url=f'http://http.tiqu.letecs.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=,&pb=4&mr=1&regions=', headers=request_header())
    # url=f'http://http.tiqu.letecs.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=1&pack=252474&ts=0&ys=0&cs=0&lb=6&sb=,&pb=4&mr=1&regions=', headers=request_header())
    j = response.text
    tr_list = j.split(',')
    # print(tr_list)
    for td in tr_list:
        t= td.split(':')
        if t[0] == '{"code"':
            return t[0]
        else:
            proxy = td.split()[0]  # 115.218.5.5:9000
            ip = test_ip(proxy, url)  # 开始检测获取到的ip是否可以使用
            if proxy == ip:
                return proxy


def test_ip(proxy, url="https://www.dianping.com/shop/G7Yc9UhIsKP88luu"):
    # 构建代理ip
    proxies = {
        "http": "http://" + str(proxy),
        "https": "http://" + str(proxy)
    }
    try:
        response = requests.get(url=url, headers=request_header(), proxies=proxies, timeout=1)  # 设置timeout，使响应等待1s
        if response.status_code == 200:
            # print(9)
            return proxy
    except:
        # if str(proxy).split(':')[1] == '121' or str(proxy).split(':')[1] == '115':
        #     return proxy  # 今日套餐已用完
        # else:
        # print(3)
        return (str(proxy)+'请求异常')
# ip = test_ip('221.203.6.14:3643')        
# print(ip)
# print('========================================1======================================')
   
url='https://www.dianping.com/shop/G7Yc9UhIsKP88luu'
proxy = send_request(url)
print('=========================================1.5=====================================')
print(proxy)
print('=========================================2=====================================')

ips = test_ip(str(proxy))
print('=========================================3=====================================')
print(ips)
print('==========================================4====================================')
if proxy == '{"code"' :
        # print(1)
        print("121今日套餐已用完  115 套餐已过期")
        proxies = ''  # 套餐过期使用本地ip
        # continue
elif  proxy== test_ip(proxy, url):  # 检测ip是否有效
    print(2)
    proxies = {
        "http": "http://" + str(proxy),
        "https": "http://" + str(proxy)
    }
else:
    print(3)
    while str(proxy)+'请求异常'  == test_ip(proxy, url):
        # 时间间隔time秒
        import time

        def sleeptime(s):
            print("休息", end="")
            for i in range(s):
                time.sleep(1)
                print("第"+str(i+1)+"秒 ", end="")
        sleeptime(2)
        proxy = send_request1(url)
        proxies = {
            "http": "http://" + str(proxy),
            "https": "http://" + str(proxy)
        }

print('==========================================5====================================')

print(proxy)

exit(0)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="is_shenzhen90_com"
    # database="is_sz"
)


mycursor = mydb.cursor()

sql = "SELECT `id`,`url`,`name` FROM ba_jzshop where id =1   order by id "
# sql = "SELECT `id`,`url`,`name` FROM ba_jzshop  where id =8  order by id"
# sql = "SELECT `*`, lag (`price`, 1, 0) over (ORDER BY `name`) AS tprice,lag (`sale`, 1, 0) over (ORDER BY `name`) as tsale FROM ba_jz_project WHERE pid = 4 and time>=1666713600 and name in(SELECT name FROM ba_jz_project WHERE time >=1666713600 and pid=4  GROUP BY name HAVING count(name) =2) "
mycursor.execute(sql)
url_list = mycursor.fetchall()

for ur in url_list:
    id = ur[0]
    url = ur[1]
    sql = "SELECT id,url FROM ba_jz_project WHERE time = '1666713600'  and pid = " + \
        str(id)
    mycursor.execute(sql)
    xmdata = mycursor.fetchall()

    print(xmdata)
    for ui in xmdata:
        i = ui[0]
        print(i)
url = urlparse('https://www.dianping.com/node/universe-sku/advance/product-detail?pf=dppc&productid=721682866&shopid=1272685953&shopuuid=k9ypzsctozzfiJMD')
paral = parse.parse_qsl(url.query)
print(paral)
pid = paral[1][1]
sid = paral[2][1]
uid = paral[3][1]


# for ur in url_list:
#     id = ur[0]
#     url = ur[1]

#     sql = "SELECT id FROM ba_jz_contend WHERE time =  '" + \
#         str(time)+"' and pid = '"+str(id)+"'"
#     mycursor.execute(sql)
#     myresult = mycursor.fetchall()
#     if myresult:
#         print(id)
#         print("已存在0跳出本次循环")
#         continue  # 跳出本次循环

#     # test_ip(proxy,url)
#     # proxy = send_request(url)
#     # if test_ip(proxy) == proxy:
#     if proxy == '':
#         proxy = send_request(url)

#         print(proxy)
#         # print(0)
#     if proxy == '{"code":121' or proxy == '{"code":115':
#         # print(1)
#         print("121今日套餐已用完  115 套餐已过期")
#         proxies = ''  # 套餐过期使用本地ip
#         # continue
#     elif test_ip(proxy, url) == proxy:  # 检测ip是否有效
#         print(2)
#         proxies = {
#             "http": "http://" + str(proxy),
#             "https": "http://" + str(proxy)
#         }
#     else:
#         # print(3)
#         while test_ip(proxy, url) != str(proxy)+'请求异常':
#             # 时间间隔time秒
#             import time
#             def sleeptime(s):
#                 print("休息", end="")
#                 for i in range(s):
#                     time.sleep(1)
#                     print("第"+str(i+1)+"秒 ", end="")
#             stime = random.randint(1, 2)
#             sleeptime(stime)
#             time = int(time.mktime(date_array))  # 今天(命名出现bug 重新获取时间)
#             proxy = send_request(url)
#             proxies = {
#                 "http": "http://" + str(proxy),
#                 "https": "http://" + str(proxy)
#             }

#     print(proxy)
#     response = requests.get(url, headers=request_header(), proxies=proxies)
#     response.encoding = "utf-8"
#     # print(response.text)
#     print(type(response.text))
#     selector = parsel.Selector(response.text)
#     # selector=''
#     logo = str(selector.css('.logo::text').get()).strip()  # 出现验证问题
#     while logo == '验证中心':
#         # 睡眠时间
#         import time

#         def sleeptime(s):
#             # 时间间隔time秒
#             print("休息", end="")
#             for i in range(s):
#                 time.sleep(1)
#                 print("第"+str(i+1)+"秒 ", end="")
#         stime = random.randint(3, 4)
#         sleeptime(stime)
#         time = int(time.mktime(date_array))  # 今天(命名出现bug 重新获取时间)

#         if test_ip(proxy, url) == proxy:
#             response = requests.get(
#                 url, headers=request_header(), proxies=proxies)
#             response.encoding = "utf-8"
#             # print(response.text)
#             print(logo)
#             selector = parsel.Selector(response.text)
#             # selector=''
#             logo = str(selector.css('.logo::text').get()).strip()  # 城市
#             print(type(logo))

#         else:
#             break

#     city = str(selector.css('.J-current-city::text').get()).strip()  # 城市
#     # print('logo1'+str(logo))
#     # print('dizhi1'+str(city))
#     # exit(0)
#     city = str(selector.css('.J-current-city::text').get()).strip()  # 城市
#     if len(city) == 0 or city == 'None':
#         mycursor = mydb.cursor()
#         sql = "SELECT city FROM ba_jz_contend WHERE   pid = '" + \
#             str(id)+"' limit 0,1"  # 城市
#         mycursor.execute(sql)
#         city = filter_string(str(mycursor.fetchone()))

#     sname = str(selector.css('.shop-name::text').get()).strip()  # 店名
#     if len(sname) == 0 or sname == 'None':
#         sname = ur[2]
#     # n
#     print(url)
#     print(city)
#     print(sname)
#     # print('sss')
#     # print(len(city))
#     # print(len(sname))
#     j = json.dumps(response.text)
#     a = json.loads(j)

#     soup = BeautifulSoup(a, 'html.parser')
#     company_item = soup.find_all('a', class_="small")
#     hot = soup.find_all('a', class_="block-link")
#     hot = str(hot)
#     hot = BeautifulSoup(hot, 'html.parser')
#     hot = hot.find_all('a')
#     # print(len(hot))
#     # exit(0)
#     company_item = str(company_item)
#     company_item = BeautifulSoup(company_item, 'html.parser')
#     t1 = company_item.find_all('a')
#     # print(t1)
#     href_list = []
#     if (len(hot) > 2):
#         hot1 = hot[0].get('href')
#         hot2 = hot[1].get('href')
#         href_list.append(hot1)
#         href_list.append(hot2)
#     for t2 in t1:
#         t3 = t2.get('href')
#         href_list.append(t3)
#     cp = 0
#     cs = 0
#     con = 0  # 项目总数
#     if len(href_list) == 0 or href_list == 'None':
#         sql = "SELECT id,url FROM ba_jz_project WHERE time =  '" + \
#             str(ztime)+"' and pid = '"+str(id)+"'"  # 检测数据是否存
#         mycursor.execute(sql)
#         href_lis = mycursor.fetchall()
#         # print(href_lis)
#         if href_lis:
#             for i in href_lis:
#                 href_list.append(i[1])
#         # print('sql1')
#     for i in href_list:
#         if len(i) > 50:

#             url = urlparse(i)
#             paral = parse.parse_qsl(url.query)
#             pid = paral[1][1]
#             sid = paral[2][1]
#             uid = paral[3][1]

#             urlp = 'https://www.dianping.com/node/universe-sku/advance/product-detail?pf=dppc&productid=' + \
#                 str(pid)+'&shopid='+str(sid)+'&shopuuid='+str(uid)

#             sql = "SELECT pid FROM ba_jz_project WHERE time =  '" + \
#                 str(time) +"' and name = '"+str(urlp) + "' and pid = '"+str(id)+"'"  # 检测数据是否存
#             mycursor.execute(sql)
#             myresult = mycursor.fetchall()
#             # myresult = ''
#             if myresult:
#                 # print("已存在")
#                 print(id)
#             else:
#                 # print("不存在")
#                 sql = "insert into ba_jz_project (time,url,pid) values ('"+str(time)+"','"+str(urlp)+"','"+str(id)+"')"  # 数据入库
#                 mycursor.execute(sql)
#             mydb.commit()
