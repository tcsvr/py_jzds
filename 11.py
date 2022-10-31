import datetime
import time
# import parsel
import re
from urllib import parse
from urllib.parse import urlparse
from bs4 import BeautifulSoup

import re
# 通过re过滤除中英文及数字以外的其他字符
def filter_string(des_string, re_string=''):
    res = re.compile("[^\\u4e00-\\u9fa5^a-z^A-Z^0-9]")
    return res.sub(re_string, des_string)
st =filter_string('半永久美瞳线 睁眼有神 灵动眼眸 • 含补色1次')
print(st)
# w=datetime.datetime.today().date()
# r=datetime.datetime.today().date() - datetime.timedelta(days=1)#格式化时间
# print(w)
# print(r)

# # 1、时间字符串转成时间数组形式
# date_array = time.strptime(str(w), "%Y-%m-%d")
# # 2、查看时间数组数据
# # print("时间数组：", date_array)
# # 3、mktime时间数组转成时间戳
# time=   int(time.mktime(date_array)) 
# print(time)

url_list=[
    'https://www.dianping.com/shop/G7Yc9UhIsKP88luu',
    'https://www.dianping.com/shop/l9pH11K90f0a9dDA',
    'https://www.dianping.com/shop/l5kzDxpJs4vd1LGQ',
    'https://www.dianping.com/shop/H3jIjng6tblpk41Y',
]
for url in url_list:
    
    print(url)
url = 'https://www.dianping.com/shop/G7Yc9UhIsKP88luu'

# # shop = re.findall("shop/(.*?)",url)[0]
# shop =url.split('shop/')[1]
# print(shop)
# w=datetime.datetime.today().date()
# r=datetime.datetime.today().date() - datetime.timedelta(days=1)#格式化时间
# wjm= str(shop)+str(w)
# print(wjm)