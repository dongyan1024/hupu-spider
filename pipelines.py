# -*- coding: utf-8 -*-
from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors
from scrapy.crawler import Settings as settings
import threading
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class HupuPipeline(object):
    def process_item(self, item, spider):
        return item

class MySQLAsyncPipeline:

    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'scrapy')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', '123456')

        self.dbpoll = adbapi.ConnectionPool('pymysql', host=host, port=port, db=db, user=user, passwd=passwd,)

    def close_spider(self, spider):
        self.dbpoll.close()

    def process_item(self, item, spider):
        self.dbpoll.runInteraction(self.insert_db, item)

        return item
    def insert_db(self, tx, item):
        values = (
            item['name'],
            item['quantity'],
            item['gender'],
            item['home'],
            item['prestige'],
            item['level'],
            item['online_time'],
            item['register_time'],
        )
        sql = 'INSERT INTO hupu(name,quantity,gender,home,prestige,level,online_time,register_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

        tx.execute(sql, values)