# 数据对比
import csv
import os

#False
# import datetime
# import time
# import mysql.connector

# w=datetime.datetime.today().date()
# r=datetime.datetime.today().date() - datetime.timedelta(days=1)#格式化时间
# print(w)
# print(r)

# 1、时间字符串转成时间数组形式
# date_array = time.strptime(str(w), "%Y-%m-%d")
# # 2、查看时间数组数据
# # print("时间数组：", date_array)
# # 3、mktime时间数组转成时间戳
# time=   int(time.mktime(date_array)) 

# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="root",
#     database="is_shenzhen90_com"
# )
# # 竞争对手数据分析后台系统



# mycursor = mydb.cursor()

def compa(x, y):
    tf=os.path.exists(y)
    if tf!=True:
        y=x
        dt=[0,0,0,0,]
        return dt 
    # with open(x, "r", encoding="gbk") as f:
    with open(x, "r", encoding="ANSI") as f:
        red = csv.reader(f)
        count = 0
        up = 0
        dw = 0
        seal = 0
        sea = 0
        xz = 0
        js = 0
        re = []
        data=[]
        # i = int()
        for r in red:
            re.append(r)
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
                    # print(r)
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
        # print(1)
        for j in da:  # 项目减少判断
            fla = 0
            fl = 0
            for r in re:
                if r == j:
                    # print(j)
                    fla = 1
                    break
            if fla == 0:
                # print(j)
                for r in re:
                    if j[0] == r[0]:
                        fl = 1
                        break
                if fl == 0:
                    # print(j)
                    js = js+1
                    

        data.append(up)           
        data.append(dw)           
        data.append(xz)           
        data.append(js)           
        data.append(seal)           
        return data
        # print("相同的数据总共有：", count)
        # print("涨价的数据总共有：", up)
        # print("降价的数据总共有：", dw)
        # print("项目新增上架：", xz)
        # print("项目减少下架：", js)
        # print("日售：", seal)
        # print("退货：", sea)


# if __name__ == "__main__":
name = '静和医疗美容(人民广场店)'
city = '上海'
cs = 665
x='l5kzDxpJs4vd1LGQ2022-10-25.csv'
y='l5kzDxpJs4vd1LGQ2022-10-24.csv'
datas=compa(x,y)
print(datas)
# sql = "SELECT * FROM ba_contend WHERE time =  '"+str(time)+"' and name = '"+name+"'"
# mycursor.execute(sql)
# myresult = mycursor.fetchall()
# print(myresult)

# if myresult:
#     print("已存在")
# else:
#     print("不存在")
#     sql = "insert into ba_contend (name, sale,sales,time,city,rprice,tprice,shelves,tshelves) values ('"+name+"','"+str(datas[4])+"','"+str(cs)+"','"+str(time)+"','"+city+"','" +str(datas[0])+"','"+str(datas[1])+"','"+str(datas[2])+"','"+str(datas[3])+"')"
#     mycursor.execute(sql)
# mydb.commit()