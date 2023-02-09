'''
Description: 网站自动登录签到
Author: 
Date: 2023-01-04 16:40:18
LastEditTime: 2023-01-12 09:45:34
LastEditors:  
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
# print(30.7+34+99+158+20+19.9+350+110+100+20.7+47.69+23+19+22.98+22.99+35.8+26.16+25.56+30.7+26.59+25.8+24.6+45.6+21.3+21.9+24.7+18.31+89+10+21.9+20.9+14.8+38.8+43.2+19.7+33.99+22.6+22.3+9.9+14+21.4+25.7+39.39+23.8+17.8+14.8+22.39+24.6+17)
# exit(0)
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
s = f'当前时间={now}\n'
print(s)

with open('log.txt', 'a') as f:
    f.write(s)
time.sleep(5)


wd = webdriver.Chrome()
wd.implicitly_wait(10)

wd.get('http://jahttp.zhimaruanjian.com/getapi/')

content = wd.find_element(By.XPATH, '//*[@class="login"]')
content.click()

input = wd.find_element(By.XPATH, '//*[@id="login_phone"]')
input.send_keys('17303169207')
# input.send_keys('13265430548')
password = wd.find_element(By.XPATH, '//*[@id="login_password"]')
password.send_keys('7710586zxc')
# password.send_keys('zc123123')

# button_login = wd.find_element(By.XPATH,
#     '//*[@id="login"]/a')
# button_login.click()
# wd.find_element(By.XPATH,
#     '//*[@id="popup-ann-modal"]/div/div/div[3]/button').click()
time.sleep(5)
wd.find_element(By.XPATH, '//*[@id="login"]').click()
try:
    time.sleep(10)
    wd.find_element(By.XPATH, '//*[@id="get_free_day_package"]').click()
    print("已领取1")
    with open('log.txt', 'a') as f:
        f.write('已领取1\n')

except:
    print("已领取0")
    with open('log.txt', 'a') as f:
        f.write('已领取0\n')
time.sleep(10)
wd.quit()
