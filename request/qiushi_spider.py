# coding:utf-8

import requests
from lxml import etree
import json

class QiushiSpider():
    """爬虫类"""
    def __init__(self):
        self.start_url = "https://www.qiushibaike.com/?page={}"
        self.headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36"}
        self.base_url = "https://www.qiushibaike.com"

    def get_url_list(self):
        """"""
        return [self.start_url.format(i) for i in range(1, 30)]

    def parer_url(self, url):
        """"""
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def get_content_detail(self, url):
        """"""
        ret = self.parer_url(url)
        r = etree.HTML(ret)
        img_list = r.xpath("//div[@class='content-img']/img/@src")
        images = []
        for img in img_list:
            images.append(img)
        return ",".join(images)



    def get_conent_list(self, html):
        """"""
        html_str_list = etree.HTML(html)
        htmls_dict = []
        rets = html_str_list.xpath("//article")
        for ret in rets:
            htmls = {}
            htmls["title"] = ret.xpath(".//div[@class='text-box']/text()")
            htmls["url"] = self.base_url + ret.xpath("./a[@class='content']/@href")[0]
            htmls["content"] = self.get_content_detail(htmls["url"])

            htmls_dict.append(htmls)
        return htmls_dict

    def save_content(self, html):
        """"""
        ii = len(html)
        count = 1
        with open("qiushi.json", "w", encoding="utf-8") as f:
            for html_str in html:
                count += 1
                f.write(json.dumps(html_str, ensure_ascii=False, indent=2))
                if ii != count:
                    f.write(",")

    def run(self):
        """实行主要逻辑"""
        for url in self.get_url_list():
            html_str = self.parer_url(url)
            html_dict = self.get_conent_list(html_str)
            self.save_content(html_dict)


if __name__ == '__main__':
    qiushispider = QiushiSpider()
    qiushispider.run()

