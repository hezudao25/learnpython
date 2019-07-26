# coding:utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

driver.get("http://www.waigf.com")


driver.find_element_by_xpath("//span[@class='user']/a[2]").click()
driver.maximize_window()
driver.save_screenshot("waigf.jpg")
driver.find_element_by_id("logusernaame").send_keys("13567890123")
driver.find_element_by_id("logpassword").send_keys("111111")

#driver.find_element_by_xpath("//button[@class='regedit-tj']").click()
#driver.find_element_by_xpath("//button[@class='regedit-tj']").send_keys(Keys.ENTER)
# 模拟JS
driver.execute_script('login()')
time.sleep(2)

driver.save_screenshot("login.jpg")

time.sleep(2)
driver.close()
driver.guit()

