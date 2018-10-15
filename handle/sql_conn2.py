#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql


class Mysql(object):

    def __init__(self):
        self.db = 0
        self.cursor = 0
        self.n_exe = 0
        self.n_commit = 0
        self.openSQL()

    def openSQL(self):
        # 打开数据库连接
        self.db = pymysql.connect(
            host="localhost", user="root", passwd="1q2w3e4r", charset='UTF8', database='topo_data')
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()
        # print("数据库连接成功", self.db, flush=True)

    def exe(self, string, args=None):
        # 使用execute方法执行SQL语句
        # select table_name from information_schema.tables where
        # table_schema=''
        if args:
            self.cursor.execute(string, args)
        else:
            self.cursor.execute(string)

    def exemany(self, string, param):
        try:
            self.cursor.executemany(string, param)
        except Exception as e:
            print(e)

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def results(self):
        # 使用 fetchone() 方法获取一条数据库。
        return self.cursor.fetchall()

    # def exe_final(self)：

    def closeSQL(self):
        # 关闭数据库连接
        # print("数据库连接关闭", flush=True)
        self.db.close()
