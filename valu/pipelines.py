# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import smtplib
import csv
import sys
import os
from selenium import webdriver
from requests_oauthlib import OAuth1Session
#from email.mime.text import MIMEText
#from email.header import Header

class ValuPipeline(object):
    def open_spider(self, spider):

        settings = spider.settings

        params = {
            'host': settings.get('MYSQL_HOST','localhost'),
            'db': settings.get('MYSQL_DATEBASE','****'),
            'user': settings.get('MYSQL_USER','****'),
            'passwd': settings.get('MYSQL_PASSWORD','****'),
            'charset': settings.get('MYSQL_CHARSET','****'),
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
            if float(item['price']) > 4.0:
                self.forserver(item)
                self.twitter(item)
        return item

    def forserver(self, item):
        driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
        driver.get("https://valu.is/login")
        btn = driver.find_element_by_class_name('btn_fb_rgst')
        btn.click()
        fa_user = '*****'#変数
        fa_pass = '*****'#変数

        input_user = driver.find_element_by_name('email')
        input_pass = driver.find_element_by_name('pass')
        input_user.send_keys(fa_user)
        input_pass.send_keys(fa_pass)
        btn = driver.find_element_by_id('loginbutton')
        btn.click()
        driver.get(item['link'])

        amount = '3'#変数
        input_amount = driver.find_element_by_id('input_amount')
        input_amount.send_keys(amount)

        input_price = float(driver.find_element_by_xpath("//input[@class = 'buy_hope_amount']").get_attribute('value')) * 2.0
        price = str(input_price)
        input_price = driver.find_element_by_id('input_rate').clear()
        input_price = driver.find_element_by_id('input_rate')
        input_price.send_keys(price)
        btn = driver.find_element_by_xpath("//input[@class = 'btn_go_confirm gc_buy']")
        btn.click()
        btn = driver.find_element_by_name('agree')
        btn.click()
        btn = driver.find_element_by_name('agree_investment')
        btn.click()
        btn = driver.find_element_by_xpath("//input[@class = 'btn_go_confirm gc_buy']")
        btn.click()
        driver.close()

    def twitter(self, item):
        twitter = OAuth1Session("*", "*")
        params = {"status": '新着きたよん\n' + '名前:' + '  ' + item['name'] + '\n' + '職業:' + '  ' + item['job'] + '\n' + '時価総額:' + '  ' + item['price'] +'[BTC]' + '\n' + '\n' '●購入リンク' + '\n' + item['link']}
        req = twitter.post("https://api.twitter.com/1.1/statuses/update.json", params = params)

    """
    def purchase(self, item):
        display = Display(visible=0, size=(800, 600))
        display.start()

        binary = FirefoxBinary('/usr/bin/firefox')
        binary.add_command_line_options('-headless')
        driver = webdriver.Firefox(firefox_binary=binary)
        driver.get("https://valu.is/login")
        btn = driver.find_element_by_class_name('btn_fb_rgst').click()
        fa_user = '******'
        fa_pass = '******'

        input_user = driver.find_element_by_name('email')
        input_pass = driver.find_element_by_name('pass')
        input_user.send_keys(fa_user)
        input_pass.send_keys(fa_pass)
        btn = driver.find_element_by_id('loginbutton').click()
        driver.get(item['link'])
        #btn = driver.find_element_by_class_name('btn_vl_buy').click()
        amount = '2'
        input_amount = driver.find_element_by_id('input_amount')
        input_amount.send_keys(amount)

        #price = item['now']
        #input_price = driver.find_element_by_id('input_rate').clear()
        input_price = driver.find_element_by_id('input_rate')
        print(input_price)
        price = float(input_price) * 2
        input_price = driver.find_element_by_id('input_rate').clear()
        input_price.send_keys(price)
        btn = driver.find_element_by_xpath("//input[@class = 'btn_go_confirm gc_buy']").click()
        btn = driver.find_element_by_name('agree').click()
        btn = driver.find_element_by_name('agree_investment').click()
        btn = driver.find_element_by_xpath("//input[@class = 'btn_go_confirm gc_buy']").click()
        driver.quit()

    def email(self, item):
        me = "*******"
        passwd ="*******"
        you = "******"
        titletext = 'valu新着きたよ！＠kai'
        body = 'hello!!\n' + 'name' + '\t' + item['name'] + '\n' + 'job' + '\t' + item['job'] + '\n' + 'price' + '\t' + item['price'] +'[BTC]' + '\n' + 'link' + '\t' + item['link']
        msg = MIMEText(body)
        msg['Subject'] = titletext
        msg['From'] = me
        msg['Bcc'] = you
        with smtplib.SMTP_SSL('smtp.gmail.com') as smtp:
            smtp.login('*******')
            smtp.send_message(msg)
    """
