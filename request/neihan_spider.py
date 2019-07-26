# coding:utf-8
import requests
import re


class NeihanSpider():
    """"""
    def __init__(self):
        self.start_url = "http://neihanshequ.com/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }

    def parse_url(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def get_first_page_content_list(self, html_str):
        content_list = re.findall(r"<h1 class=\"title\">.*?<p>(.*)</p>", html_str)
        return content_list

    def run(self):
        html_str = self.parse_url(self.start_url)
        html = self.get_first_page_content_list(html_str)
        print(html)


if __name__ == '__main__':
    neihan = NeihanSpider()
    neihan.run()