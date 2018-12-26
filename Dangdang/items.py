# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DangdangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    goods_id = scrapy.Field() # 商品id
    category = scrapy.Field()  # 商品类别
    title = scrapy.Field()   # 商品名称
    link = scrapy.Field()    # 商品链接
    price = scrapy.Field()   # 商品价格
    comment_num = scrapy.Field()  # 商品评论数
    good_comment_num = scrapy.Field() # 商品好评数
    mid_comment_num = scrapy.Field() # 商品中评数
    bad_comment_num = scrapy.Field() # 商品差评数
    rate = scrapy.Field()   # 商品的好评率
    source = scrapy.Field()   # 商品的来源地
    detail = scrapy.Field()   # 商品详情
    img_link = scrapy.Field() #商品图片链接

class CommentItem(scrapy.Item):
    goods_id = scrapy.Field() # 商品id
    comment = scrapy.Field() # 商品的所有评论
    score = scrapy.Field() # 评论对应的评分
    time = scrapy.Field()  # 评论的时间

