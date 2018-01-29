# -*- coding: utf-8 -*-

import redis
import pymysql


redis_handler = redis.Redis(host='localhost', port=6379, db=0)

class MysqlHandler():
    def __init__(self):
        self.conn = pymysql.connect(host='http://127.0.0.1', user='root', password='123', database='zhihu', charset='utf-8')

    def __enter__(self):
        self.cur = self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.clo
