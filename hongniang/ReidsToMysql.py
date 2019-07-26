#!/usr/bin/env python2
# -*- coding:utf-8 -*-

import redis
import json
from MysqlHelper import MysqlHelper



#获取mysql 的连接
mysql = MysqlHelper(host='127.0.0.1',port=3306, db='pythonspider2',user='root',passwd='root')
#获取redis 的连接
rediscli = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

def process_redisdata():
    """
    将redis 的数据，存放到mysql中
    :return:
    """
    while True:
        # FIFO模式为 blpop，LIFO模式为 brpop，获取键值
        source, data = rediscli.blpop(["hongniangSpiderRedis:items"])
        #data = unicode(str(data).encode('utf-8'), "utf-8")
        item = json.loads(data)

        photos = ','.join(item['photos'])
        sql = 'insert into hongniang(nickname,loveid,photos,age,height,ismarried,yearincome,education,workaddress,soliloquy,gender)  ' \
              'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)';
        params = [str(item['nickname']),str(item['loveid']),str(photos),str(item['age'])
                    ,str(item['height']),str(item['ismarried']),str(item['yearincome']),str(item['education'])
                    , str(item['workaddress']),str(item['soliloquy']),str(item['gender'])]

        insertnum = mysql.insert(sql=sql, params=params)
        if insertnum > 0:
            print("成功")


if __name__ == '__main__':
    process_redisdata()
