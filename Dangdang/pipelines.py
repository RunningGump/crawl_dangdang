# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from scrapy.conf import settings
import json
from Dangdang.items import DangdangItem
from Dangdang.items import CommentItem

## pipeline默认是不开启的，需在settings.py中开启
class DangdangPipeline(object):
    def process_item(self, item, spider):
        # 连接数据库
        conn = pymysql.connect(host="localhost",user="root",passwd='******',db="dd",use_unicode=True, charset="utf8")
        cur = conn.cursor()             # 用来获得python执行Mysql命令的方法,也就是我们所说的操作游标
        print("mysql connect success")  # 测试语句，这在程序执行时非常有效的理解程序是否执行到这一步
        # 存储当当商品信息的逻辑
        if isinstance(item, DangdangItem):
            try:
                goods_id = item["goods_id"]
                category = item["category"]
                title = item["title"]
                if len(title)>40:
                    title = title[0:40] + '...'
                link = item["link"]
                img_link = item['img_link']
                price = item["price"]
                comment_num = item["comment_num"]
                good_comment_num = item["good_comment_num"]
                mid_comment_num = item["mid_comment_num"]
                bad_comment_num = item["bad_comment_num"]
                rate = item["rate"]
                source = item["source"]
                detail = item["detail"]

                sql = "INSERT INTO goods(goods_id,category,title,price,comment_num,good_comment_num,mid_comment_num,bad_comment_num,rate,source,detail,link,img_link) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                                        (goods_id,category,title,price,comment_num,good_comment_num,mid_comment_num,bad_comment_num,rate,source,detail,link,img_link)
                print(sql)
            except Exception as err:
                print(err,'EORR1111!!!')

            '''########################################################
                        执行sql语句，将商品信息存入goods数据表             
            ########################################################'''
            try:
                cur.execute(sql)         # 真正执行MySQL语句，即查询TABLE_PARAMS表的数据
                print("insert goods success")  # 测试语句
            except Exception as err:
                print(err)
                conn.rollback() #事务回滚,为了保证数据的有效性将数据恢复到本次操作之前的状态.有时候会存在一个事务包含多个操作，而多个操作又都有顺序，顺序执行操作时，有一个执行失败，则之前操作成功的也会回滚，即未操作的状态
            else:
                conn.commit()   #当没有发生异常时，提交事务，避免出现一些不必要的错误

        elif isinstance(item, CommentItem):
            try:
                # 遍历所有评论
                goods_id = item["goods_id"]
                comment = item["comment"]
                score = item ["score"]
                comment_time = item["time"]

                sql2 = "INSERT INTO comments(goods_id,comment,score,comment_time) VALUES ('%s','%s','%s','%s')" % \
                                            (goods_id,comment,score,comment_time)
                print(sql2)
            except Exception as err:
                print(err,'EORR222!!!')

            '''########################################################
                        执行sql语句，将评论信息存入comments数据表             
            ########################################################'''
            try:
                cur.execute(sql2)         # 真正执行MySQL语句，即查询TABLE_PARAMS表的数据
                print("insert comments success")  # 测试语句
            except Exception as err:
                print(err)
                conn.rollback() #事务回滚,为了保证数据的有效性将数据恢复到本次操作之前的状态.有时候会存在一个事务包含多个操作，而多个操作又都有顺序，顺序执行操作时，有一个执行失败，则之前操作成功的也会回滚，即未操作的状态
            else:
                conn.commit()   #当没有发生异常时，提交事务，避免出现一些不必要的错误

        conn.close()  #关闭连接 



        return item   #框架要求返回一个item对象

