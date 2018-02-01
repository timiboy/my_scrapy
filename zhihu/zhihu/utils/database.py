# -*- coding: utf-8 -*-

from my_logger import MyLogger

import traceback
import pymongo
import redis
import pymysql
from pymysql.err import InterfaceError, IntegrityError
# pymysql.err.InterfaceError 连接丢失错误
# pymysql.err.IntegrityError 唯一性数据重复出现错误


redis_handler = redis.Redis(host='localhost', port=6379, db=0)
mongo_handler = pymongo.MongoClient(host='localhost', port=27017)


class MysqlHandler():
    def __init__(self, host='http://127.0.0.1', user='root', password='123', database='zhihu'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = pymysql.connect(host=host, user=user, password=password, database=database, charset='utf-8')

        self.logger = MyLogger(name='mysql')
        self.error_count = 0

    def __enter__(self):
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.error_count += 1
        if self.error_count > 3:
            return False

        if exc_type == InterfaceError:
            msg = '\n'.join(traceback.format_exception(exc_type, exc_val, exc_tb))
            self.logger.log(msg=msg)
            self.conn.rollback()
            self.conn = pymysql .conncet(host=self.host, user=self.user, password=self.password, database=self.database, charset='utf-8')
        else:
            msg = '\n'.join(traceback.format_exception(exc_type, exc_val, exc_tb))
            self.logger.log(msg=msg)
            self.conn.rollback()
        return True

    def __del__(self):
        self.cur.close()
        self.conn.close()

