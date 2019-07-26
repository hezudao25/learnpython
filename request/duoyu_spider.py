# coding:utf-8
from selenium import webdriver
import time

class DouyuSpider():
    """lei"""
    def __init__(self):
        self.start_url ="https://www.douyu.com/directory/all"
        self.driver = webdriver.Chrome()

    def get_content_list(self):
        li_list = self.driver.find_elements_by_xpath("//ul[@class='layout-Cover-list']/li")
        content_list = []

        for li in li_list:
            items = {}
            print(li)
            imgs = li.find_elements_by_xpath(".//div[@class='DyListCover-imgWrap']//img")
            imgs = imgs[0] if len(imgs) > 0 else None
            items["img"] = imgs

            #items["title"] = li.find_element_by_xpath(".//h3[@class='DyListCover-intro']").text
            content_list.append(items)

        # 获取下一页
        next_url = self.driver.find_elements_by_xpath("//span[@class='dy-Pagination-item-custom']")
        next_url = next_url[0] if len(next_url) > 0 else None
        return content_list, next_url

    def save_content(self, content):
        pass


    def run(self):
        # 1. start_url

        # 2. 发送请求，获取响应
        self.driver.get(self.start_url)
        # 3. 提取数据，提取下一页元素
        content_list, next_url = self.get_content_list()
        # 4. 保持数据
        self.save_content(content_list)
        # 5. 点击下一页 进行循环
        while next_url is not None:
            next_url.click()
            time.sleep(2)
            content_list, next_url = self.get_content_list()
            self.save_content(content_list)

        self.driver.quit()


if __name__ == '__main__':
    douyuspider = DouyuSpider()
    douyuspider.run()