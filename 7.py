#评论系统
from cgi import print_arguments
import requests
import parsel
import csv
import re
from lxml import etree
from scrapy import Selector
import json
import mysql.connector


# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   passwd="root",
#   database="is_shenzhen90_com"
# )
#评论系统

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="is_shenzhen90_com"
    # database="is_sz"
)
mycursor = mydb.cursor()

# f =open('6.csv', 'w', newline='')
# csv_writer = csv.DictWriter(f, fieldnames=[
#         '评论',
#         '评论时间',
#         '用户id',
#         '用户名',
#         '平台',
#         # '环境',
#         # '服务',
#         # '地址',
#         # '电话',
#         # '详情页',
# ])
#  admin_id  妇科 = 16 ; 产科=22;  美容=20; 体检=18; 口腔=25;眼科=28；
# csv_writer.writeheader()


for x in range(2,108):
    # url = 'https://www.meituan.com/ptapi/poi/getcomment?id=193992083&offset='+str(x)+'0&pageSize=10&mode=0&starRange=&userId=&sortType=1'
    url = 'https://www.meituan.com/ptapi/poi/getcomment?id=94271915&offset='+str(x)+'0&pageSize=10&mode=0&sortType=1'
    # url = 'https://i.meituan.com/xiuxianyule/api/getCommentList?poiId=65145272&offset='+str(x)+'0&pageSize=10&sortType=1&mode=0&starRange=10%2C20%2C30%2C40%2C50&tag=%E5%85%A8%E9%83%A8'

    # print(url)
    headers = {
        'Host': 'www.meituan.com',
        'Referer': 'https://www.meituan.com/cate/86541740/',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        "Cookie": '_lxsdk_cuid=1827caf303a6e-0798f32faa8b07-3b3d5203-1fa400-1827caf303bc8; latlng=22.547504%2C114.114024; ci3=30; uuid=ddfa89fbd2594297811d.1661133248.1.0.0; ci=20; rvct=20%2C50%2C30; firstTime=1661133491577; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=182d2e835be-18a-30b-668%7C%7C7'
        # "Cookie": 'uuid=975e7cc8fa0248a4bf76.1659949858.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=1827cb8c18313-0b20aa4b06635e-9126f2c-1fa400-1827cb8c184c8; webloc_geo=22.537385%2C114.121545%2Cwgs84; ci=30; rvct=30%2C1; qruuid=7ad2a629-827f-493b-8efc-d8179ea27f5a; token2=ZmKdZAqaSfgTbNTX4e2plLH_enMAAAAAUhMAAGRkZs_zBPuWn5MMONYLaqLPLimxHZV8IZa3S3XttTjbtah1THMU6tEhStcOAEAwDQ; oops=ZmKdZAqaSfgTbNTX4e2plLH_enMAAAAAUhMAAGRkZs_zBPuWn5MMONYLaqLPLimxHZV8IZa3S3XttTjbtah1THMU6tEhStcOAEAwDQ; lt=ZmKdZAqaSfgTbNTX4e2plLH_enMAAAAAUhMAAGRkZs_zBPuWn5MMONYLaqLPLimxHZV8IZa3S3XttTjbtah1THMU6tEhStcOAEAwDQ; u=237742934; n=SvJ610711434; unc=SvJ610711434; firstTime=1659949906686; _lxsdk_s=1827cb8c185-84a-e73-848%7C%7C31'
    }

    response = requests.get(url, headers=headers)
    # print(type(response.text))
    selector = parsel.Selector(response.text)
    j = json.loads(response.text)
    # title = selector.css('.seller-name::text').get()  # 店名
    # print(response.text)
    # print(response.text)
    # count = selector.css('p::text').extract()
    # print(j)
    # j = json.loads(count[0])
    # print(j)
    # print(j['data']['commentDTOList'])
    # con = (j['data']['commentDTOList'])#wap端评论
    con = (j['comments'])#pc端评论
    # print(con)

    for i in con:
        # count = i['comment'].replace('\U0001f44d', '')  # 评论
        count = re.sub("[^，。\\u4e00-\\u9fa5^a-z^A-Z^0-9^%&',.;=?$\x22]", "", i['comment'])   # 评论
        count = count.replace('劲松','')  # 评论过滤
        count = count.replace("'",'"')  # 评论过滤
        commentTime = i['commentTime']  #评论时间
        userId = i['userId']  # 用户id
        print(x)
        print('===')
        print(str(i['userId']))
        userName = i['userName']  # 用户名
        platform = '美团_劲松口腔医院（外企院）'  # 平台
        star=i['star']#评分
        print(star)
        if star >=30:#3颗星以上数据
            #数据库插入
            if count != '' and len(count) >16:
                sql = "SELECT * FROM ba_review_system WHERE platform = '"+platform+"' and commentime = '"+commentTime+"' and userid = '"+str(userId)+"' and username = '"+userName+"'"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                if myresult:
                    print("已存在")
                else:
                    print("不存在")#  admin_id  妇科 = 16 ; 产科=22;  美容=20; 体检=18; 口腔=25;眼科=28；
                    sql = "insert into ba_review_system (comments, platform,commentime,userid,username,admin_id) values ('"+count+"','"+platform+"','"+commentTime+"','"+str(userId)+"','"+userName+"','25')"
                    mycursor.execute(sql)
                mydb.commit()

        
    #     Price = count[i]['comment'] # 人均消费
    #     item_list = selector_1.css('#comment_score .item::text').getall()  # 评价
    #     taste = item_list[0].split(': ')[-1]  # 口味评分
    #     environment = item_list[1].split(': ')[-1]  # 环境评分
    #     service = item_list[-1].split(': ')[-1]  # 服务评分
    #     address = selector_1.css('#address::text').get()  # 地址
    #     tel = selector_1.css('.tel ::text').getall()[-1]  # 电话
        # dit = {
        #     '评论': count,
        #     '评论时间': commentTime,
        #     '用户id': userId,
        #     '用户名': userName,
        #     '平台': platform,
        #     # '环境': environment,
        #     # '服务': service,
        #     # '地址': address,
        #     # '电话': tel,
        #     # '详情页': index,
        # }
        # csv_writer.writerow(dit)