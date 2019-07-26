# coding:utf-8

import requests
import json
import re


class DoubianSpider():
    """"""
    def __init__(self):
        self.start_url = "https://m.douban.com/rexxar/api/v2/subject_collection/movie_showing/items?os=android&for_mobile=1&callback=jsonp1&start=0&count=18&loc_id=108288&_=0"
        self.headers = {"Host": "m.douban.com",
                        "Referer": "https://m.douban.com/movie/nowintheater?loc_id=108288",
                        "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36"
                        }

    def parse_url(self, url):
        """post"""
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def get_json_content_list(self, html_str):
        html_str = re.findall(";jsonp1\((.*?)\);", html_str)
        for _html_str in html_str:
             json_str = json.loads(_html_str)

        with open("doubian.json", "w", encoding="utf-8") as f:
            for str in json_str["subject_collection_items"]:
                f.write(json.dumps(str, indent=2, ensure_ascii=False))
                f.write("\n")

    def run(self):
        """主要动作"""
        # 1
        html_str = self.parse_url(self.start_url)
        # 2
        self.get_json_content_list(html_str)


if __name__ == '__main__':
    doubian = DoubianSpider()
    doubian.run()