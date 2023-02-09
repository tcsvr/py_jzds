from selenium import webdriver
from selenium.webdriver import ActionChains
import time

# browser = webdriver.Firefox()
# browser.get('https://www.dianping.com/shop/H5YifLwJ4Rzl5PG9')

# time.sleep(2)
# gundongz = browser.find_element_by_xpath('//*[@id="yodaBox"]/div[3]')
# # 点击该元素并且不放开
# ActionChains(browser).click_and_hold(gundongz).perform()
# # 滑动该元素
# ActionChains(browser).move_by_offset(xoffset=300, yoffset=0).perform()
# # 放开该元素
# ActionChains(browser).release().perform()
# time.sleep(2)
# # browser.find_element_by_id('btn-submit').click()
# from selenium import webdriver
# import unittest
# from selenium.webdriver import ActionChains
# import time
 
 
url = "https://www.dianping.com/shop/H5YifLwJ4Rzl5PG9"
driver = webdriver.Chrome(executable_path="C:chromedriver.exe")
driver.get(url)
driver.maximize_window()
 # 获取第一，二，三能拖拽的元素
drag1 = driver.find_element_by_id("yodaBox")
 
# 创建一个新的ActionChains，将webdriver实例对driver作为参数值传入，然后通过WenDriver实例执行用户动作
action_chains = ActionChains(driver)
# 将页面上的第一个能被拖拽的元素拖拽到第二个元素位置
# 将页面上的第三个能拖拽的元素，向右下拖动10个像素，共拖动5次
action_chains.drag_and_drop_by_offset(drag1, 208, 0).perform()
time.sleep(5)
driver.quit()
