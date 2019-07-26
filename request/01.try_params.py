# coding:utf-8

import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
params = {"wd": "王玉琦"}
url_temp = "https://www.baidu.com/s?"
r = requests.get(url_temp, headers=headers, params=params)
print(r.status_code)
print(r.request.url)