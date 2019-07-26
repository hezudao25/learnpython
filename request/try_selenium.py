# coding:utf-8

from selenium import webdriver
import time


#driver = webdriver.Chrome()
driver = webdriver.PhantomJS()

driver.get("http://www.baidu.com")

driver.find_element_by_id("kw").send_keys("王玉琦")
driver.find_element_by_id("su").click()

driver.maximize_window()
driver.save_screenshot("baidu.jpg")

time.sleep(5)
driver.quit()