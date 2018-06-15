# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import csv
import sys
import os

class ValuPipeline(object):
    def open_spider(self, spider):

        settings = spider.settings

        params = {
            'host': settings.get('MYSQL_HOST','localhost'),
            'db': settings.get('MYSQL_DATEBASE','mydb'),
            'user': settings.get('MYSQL_USER','dbuser'),
            'passwd': settings.get('MYSQL_PASSWORD','kaikai'),
            'charset': settings.get('MYSQL_CHARSET','utf8mb4'),
        }

        self.conn = MySQLdb.connect(**params)
        self.c = self.conn.cursor()
        #self.c.execute('''CREATE TABLE IF NOT EXISTS items(id INTEGER NOT NULL AUTO_INCREMENT,name text NOT NULL,price text NOT NULL,job text NOT NULL,PRIMARY KEY(id))''')
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        t = 0
        sql = "SELECT name FROM items"
        self.c.execute(sql)

        results = self.c.fetchall()
        for r in results:
            print(r)
            #m = "('" + item['name'] + "',)"
            if item['name'] in r:
                    print(item['name'])
                    print("同じ")
                    t = 1


            #self.c.execute('INSERT INTO items(job) VALUES(%(job)s)',dict(item))
            #self.c.execute('INSERT INTO items(price) VALUES(%(price)s)',dict(item))

        if t == 1:
            print("---------------------------")
            print(item['name'])
            print("とったことある（笑）")
            print("---------------------------")

        if t == 0:
            print("---------------------------")
            print(item['name'])
            print("新着！！")
            print("---------------------------")
            #self.c.execute('DELETE FROM items')
            self.c.execute('INSERT INTO items(name) VALUES(%(name)s)',dict(item))
            self.conn.commit()
            if float(item['price']) > 3.0:
                self.email(item)
        return item

    def email(self, item):
        me = "valucrawler@gmail.com"
        passwd ="valuvalu7"
        you = "abebe1128@gmail.com,kaikaikai8217@gmail.com"
        titletext = 'valu新着きたよ！＠kai'
        body = 'hello!!\n' + 'name' + '\t' + item['name'] + '\n' + 'job' + '\t' + item['job'] + '\n' + 'price' + '\t' + item['price'] +'[BTC]' + '\n' + 'link' + '\t' + item['link']

        msg = MIMEText(body)
        msg['Subject'] = titletext
        msg['From'] = me
        msg['Bcc'] = you


        with smtplib.SMTP_SSL('smtp.gmail.com') as smtp:
            smtp.login('valucrawler@gmail.com','valuvalu7')
            smtp.send_message(msg)
