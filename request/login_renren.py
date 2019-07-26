# coding:utf-8

import requests

session = requests.session()
port_url = "http://www.renren.com/Plogin.do"
post_data = {"email": "mr_mao_hacker@163.com", "password": "alarmchime"}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
# 使用session发送post请求，cookies保存其中
session.post(port_url, data=post_data, headers=headers)
r = requests.get("http://www.renren.com/327550029/profile", headers=headers)

with open("renren.html", "w", encoding="utf-8") as f:
    f.write(r.content.decode())

