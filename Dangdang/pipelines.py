# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from scrapy.conf import settings

## pipeline默认是不开启的，需在settings.py中开启
class DangdangPipeline(object):
    def process_item(self, item, spider):
        ##建立数据库连接
        conn = pymysql.connect(host="localhost",user="root",passwd='940212',db="dd",use_unicode=True, charset="utf8")
        cur = conn.cursor()             # 用来获得python执行Mysql命令的方法,也就是我们所说的操作游标
        print("mysql connect success")  # 测试语句，这在程序执行时非常有效的理解程序是否执行到这一步
        try:
            category = item["category"]
            title = item["title"]
            if len(title)>40:
                title = title[0:40] + '...'
            link = item["link"]
            img_link = item['img_link']
            price = item["price"]
            comment = item["comment"]
            rate = item["rate"]
            source = item["source"]
            detail = item["detail"]

            sql = "INSERT INTO goods(category,title,price,comment,rate,source,detail,link,img_link) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (category,title,price,comment,rate,source,detail,link,img_link)
            print(sql)
        except Exception as err:
            pass

        try:
            cur.execute(sql)         # 真正执行MySQL语句，即查询TABLE_PARAMS表的数据
            print("insert success")  # 测试语句
        except Exception as err:
            print(err)
            conn.rollback() #事务回滚,为了保证数据的有效性将数据恢复到本次操作之前的状态.有时候会存在一个事务包含多个操作，而多个操作又都有顺序，顺序执行操作时，有一个执行失败，则之前操作成功的也会回滚，即未操作的状态
        else:
            conn.commit()   #当没有发生异常时，提交事务，避免出现一些不必要的错误

        conn.close()  #关闭连接

        return item   #框架要求返回一个item对象

