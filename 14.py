from tkinter import N
import mysql.connector
import time
import re
from re import T
import datetime


def filter_string(des_string, re_string=''):
    res = re.compile("[^\\u4e00-\\u9fa5^a-z^A-Z^0-9]")
    return res.sub(re_string, des_string)
# A = range(0,10)
# B = range(0,20)
# C = list(set(B) - set(A))
# union = list(set(A)|set(B))
# insect = list(set(A)&set(B))

# print(list(A))
# print(B)
# print(C)
# print(union)
# print(insect)
# exit(0)

w = datetime.datetime.today().date()
zt = datetime.datetime.today().date() - datetime.timedelta(days=1)  # 格式化时间
date_array = time.strptime(str(w), "%Y-%m-%d")
date_arrayz = time.strptime(str(zt), "%Y-%m-%d")
# print(date_array)
# print(date_arrayz)
time = int(time.mktime(date_array))#今天
ztime = int(time)-24*60*60#昨天
ztime = 1667836800  # time的昨天

print(time)
print(ztime)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="is_shenzhen90_com"
    # database="is_sz"
)
mycursor = mydb.cursor()
sql = "SELECT city FROM ba_jz_contend WHERE  pid = 1 limit 0,1"  # 检测数据是否存
mycursor.execute(sql)
city = filter_string(str(mycursor.fetchone()))

print(city)
exit(0)
sql = "SELECT id,url FROM ba_jz_project WHERE time =  '" + \
    str(ztime)+"' and pid = 1"  # 检测数据是否存
mycursor.execute(sql)
href_lis = mycursor.fetchall()
print(1)
for i in href_lis:
    print(i[1])
    
exit(0)    
id=3
# print(type(id))
rsale =0
rtsale =0
rprice=0
tprice=0
shelves=0
tshelves=0

# sql = "SELECT id FROM ba_jz_project WHERE time =  '"+str(ztime)+"' and pid = '"+str(id)+"' limit 0,1"
# mycursor.execute(sql)
# ztdata = mycursor.fetchall()
# if ztdata:#昨天的数据存在
#     print(ztdata)
# exit(0)    
sql="SELECT `name`,`sale`,`price`,`pid`  FROM ba_jz_project WHERE time="+str(time)+" and pid="+str(id)+" and name in(SELECT name FROM ba_jz_project WHERE time >="+str(ztime)+" and pid="+str(id)+" GROUP BY name HAVING count(name) =2) ORDER BY `name`"
# sql="SELECT `name`,`sale`,`price`,`pid`  FROM ba_jz_project WHERE time="+str(time)+" and name in(SELECT name FROM ba_jz_project WHERE time >="+str(ztime)+"  GROUP BY name HAVING count(name) =2) ORDER BY `name`"
# sql="SELECT *  FROM ba_jz_project WHERE time="+str(time)+" and pid="+str(id)+" and name in(SELECT name FROM ba_jz_project WHERE time >="+str(ztime)+" and pid="+str(id)+" GROUP BY name HAVING count(name) =2) ORDER BY `name`"
# sql="SELECT *  FROM ba_jz_project WHERE time="+str(time)+"  and name in(SELECT name FROM ba_jz_project WHERE time >="+str(ztime)+"  GROUP BY name HAVING count(name) =2) ORDER BY `name`"
mycursor.execute(sql)
name_list = mycursor.fetchall()# name 相同的数据

sql="SELECT `name`,`sale`,`price`,`pid` FROM ba_jz_project WHERE time ="+str(ztime)+" and pid="+str(id)+" and name in(SELECT name FROM ba_jz_project WHERE time >="+str(ztime)+" and pid="+str(id)+"  GROUP BY name HAVING count(name) =2) ORDER BY `name`"
# sql="SELECT `name`,`sale`,`price`,`pid` FROM ba_jz_project WHERE time ="+str(ztime)+"  and name in(SELECT name FROM ba_jz_project WHERE time >="+str(ztime)+"   GROUP BY name HAVING count(name) =2) ORDER BY `name`"
# sql="SELECT * FROM ba_jz_project WHERE time ="+str(ztime)+" and pid="+str(id)+" and name in(SELECT name FROM ba_jz_project WHERE time >="+str(ztime)+" and pid="+str(id)+"  GROUP BY name HAVING count(name) =2) ORDER BY `name`"
# sql="SELECT * FROM ba_jz_project WHERE time ="+str(ztime)+"  and name in(SELECT name FROM ba_jz_project WHERE time >="+str(ztime)+"  GROUP BY name HAVING count(name) =2) ORDER BY `name`"
mycursor.execute(sql)
zname_list = mycursor.fetchall()# name 相同的数据


ne= (set(name_list) - set(zname_list))
en= (set(zname_list) - set(name_list))
print(len(name_list))
# print(len(ne))
print(len(zname_list))
# print(len(en))
for n in ne:
    # print(n)
    for e in en:
        # print(e)
        if(n[0]==e[0]):
            if(int(n[2])>int(e[2])):
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
            if(int(n[1])>int(e[1])):
                rsale = rsale + (int(n[1])-int(e[1]))  #售货  
            elif(int(n[1])<int(e[1])):
                rtsale = rtsale - (int(n[1])-int(e[1])) #退货
                
# print(rsale)             
# print(rtsale)             
# print(rprice)             
# print(tprice)  
# exit(0)

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
#                 rsale = rsale + (int(na[2])-int(zna[2]))  #售货  
#             elif(int(na[2])<int(zna[2])):
#                 rtsale = rtsale - (int(na[2])-int(zna[2])) #退货
            
    
# exit(0)

# sql = "SELECT `*`, lag (`price`, 1, 0) over (ORDER BY `name`) AS tprice,lag (`sale`, 1, 0) over (ORDER BY `name`) as tsale FROM ba_jz_project WHERE pid = '"+str(id)+"' and time>='"+str(ztime)+"' and name in(SELECT name FROM ba_jz_project WHERE time >='"+str(ztime)+"' and pid='"+str(id)+"'  GROUP BY name HAVING count(name) =2) "
# # sql = "SELECT `*`, lag (`price`, 1, 0) over (ORDER BY `name`) AS tprice,lag (`sale`, 1, 0) over (ORDER BY `name`) as tsale FROM ba_jz_project WHERE pid = 1 and time>=1666713600 and name in(SELECT name FROM ba_jz_project WHERE time >=1666713600 and pid=1  GROUP BY name HAVING count(name) =2) "
# # sql="SELECT `*`, lag (`price`, 1, 0) over (ORDER BY `name`) AS tprice, lag (`sale`, 1, 0) over (ORDER BY `name`) AS tsale FROM ba_jz_project WHERE pid = 4 AND time >= 1666713600 AND NAME IN ( SELECT NAME FROM ba_jz_project WHERE time >= 1666713600 and pid =4 GROUP BY NAME HAVING count(NAME) = 2)"
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
#             sale = sale + (int(ur[2])-int(ur[8]))    
#         elif(int(ur[2])<int(ur[8])):
#             tsale = tsale - (int(ur[2])-int(ur[8])) 

sql ="SELECT * FROM ba_jz_project WHERE time>="+str(ztime)+" and  name in( SELECT name FROM ba_jz_project WHERE time>="+str(ztime)+" and pid="+str(id)+" GROUP BY name HAVING count(name) =1) and pid ="+str(id)+" ORDER BY name"
# sql ="SELECT * FROM ba_jz_project WHERE time>=1666713600 and  name in( SELECT name FROM ba_jz_project WHERE time>=1666713600 and pid=4 GROUP BY name HAVING count(name) =1) and pid ="+str(id)+" ORDER BY name"
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
exit(0)        