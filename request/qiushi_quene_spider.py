# coding:utf-8

import requests
from lxml import etree
import json
import threading
from queue import Queue

class QiushiSpider():
    """爬虫类"""
    def __init__(self):
        self.start_url = "https://www.qiushibaike.com/?page={}"
        self.headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36"}
        self.base_url = "https://www.qiushibaike.com"
        self.url_quene = Queue()
        self.content_list_quene = Queue()
        self.content_detail_quene = Queue()

    def get_url_list(self):
        """"""
        for i in range(1, 3):
            self.url_quene.put(self.start_url.format(i))

    def parer_url(self):
        """"""
        while True:
            url = self.url_quene.get()
            response = requests.get(url, headers=self.headers)
            self.content_list_quene.put(response.content.decode())
            self.url_quene.task_done()

    def get_content_detail(self, url):
        """"""
        ret = self.parer_url(url)
        r = etree.HTML(ret)
        img_list = r.xpath("//div[@class='content-img']/img/@src")
        images = []
        for img in img_list:
            images.append(img)
        return ",".join(images)



    def get_conent_list(self):
        """"""
        while True:
            html = self.content_list_quene.get()
            html_str_list = etree.HTML(html)
            htmls_dict = []
            rets = html_str_list.xpath("//article")
            for ret in rets:
                htmls = {}
                htmls["title"] = ret.xpath(".//div[@class='text-box']/text()")
                htmls["url"] = self.base_url + ret.xpath("./a[@class='content']/@href")[0]
                htmls["content"] = self.get_content_detail(htmls["url"])

                htmls_dict.append(htmls)
                self.content_detail_quene.put(htmls_dict)

            self.content_list_quene.task_done()


    def save_content(self):
        """"""
        while True:
            html = self.content_detail_quene.get()
            ii = len(html)
            count = 1
            with open("qiushi.json", "w", encoding="utf-8") as f:
                for html_str in html:
                    count += 1
                    f.write(json.dumps(html_str, ensure_ascii=False, indent=2))
                    if ii != count:
                        f.write(",")

            self.content_detail_quene.task_done()

    def run(self):
        """实行主要逻辑"""
        threadings = []
        t_url = threading.Thread(target=self.get_url_list)
        threadings.append(t_url)
        for i in range(20):
            t_parer = threading.Thread(target=self.parer_url)
            threadings.append(t_parer)
        for i in range(2):
            t_content = threading.Thread(target=self.get_conent_list)
            threadings.append(t_content)
        t_save = threading.Thread(target=self.save_content)
        threadings.append(t_save)

        for thr in threadings:
            thr.setDaemon(True)
            thr.start()

        for q in [self.url_quene, self.content_list_quene, self.content_detail_quene]:
            q.join()

        print("主线程结束")


if __name__ == '__main__':
    qiushispider = QiushiSpider()
    qiushispider.run()

