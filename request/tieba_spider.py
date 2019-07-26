# coding:utf-8

import requests
import os


class TiebaSpider():
    """百度贴吧采集类"""
    def __init__(self, keywords, page_num):
        self.keywords = keywords
        self.page_num = page_num

    def get_page_list(self):
        """获取页数"""
        return [i*50 for i in range(self.page_num)]

    def reuest_url(self, page_n, current):
        """"""
        url = "http://tieba.baidu.com/f?kw={}&ie=utf-8&pn={}".format(self.keywords, page_n)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
        resp = requests.get(url, headers=headers)
        content = resp.content.decode()
        filename = os.path.join(os.path.dirname(__file__), "bieba/{}吧第{}页.html".format(self.keywords, current))
        print(filename)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

    def run(self):
        """执行采集"""

        if os.path.exists(os.path.join(os.path.dirname(__file__), "bieba")) == False:
            os.mkdir(os.path.join(os.path.dirname(__file__), "bieba"))
        page_list = self.get_page_list()
        for i in page_list:
            index = page_list.index(i) + 1
            self.reuest_url(i, index)






if __name__ == '__main__':
    spider = TiebaSpider("娱乐圈", 100)
    spider.run()