# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Dangdang.items import DangdangItem
from Dangdang.items import CommentItem
import re
import urllib.request
import json
import requests
from lxml import etree


class DdSpider(CrawlSpider):
    name = 'dd'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://category.dangdang.com/']

    # 分析网页链接，编写rules规则,提取商品详情页的链接
    rules = (
        Rule(LinkExtractor(allow=r'/cp\d{2}.\d{2}.\d{2}.\d{2}.\d{2}.\d{2}.html$|/pg\d+-cp\d{2}.\d{2}.\d{2}.\d{2}.\d{2}.\d{2}.html$', deny=r'/cp98.\d{2}.\d{2}.\d{2}.\d{2}.\d{2}.\d{2}.html'),
             follow=True),
        Rule(LinkExtractor(allow=r'/cid\d+.html$|/pg\d+-cid\d+.html$', deny=r'/cp98.\d{2}.\d{2}.\d{2}.\d{2}.\d{2}.\d{2}.html'),
             follow=True),
        Rule(LinkExtractor(allow=r'product.dangdang.com/\d+.html$', restrict_xpaths=("//p[@class='name']/a")),
             callback='parse_item',
             follow=False),      # allow与restrict_xpath配合使用,效果很好,可以更精准筛选链接.
    )

    # 解析商品详情页面
    def parse_item(self, response):
        item = DangdangItem()  # 实例化item
        commment_item = CommentItem()
        item["category"] = response.xpath('//*[@id="breadcrumb"]/a[1]/b/text()').extract_first()+'>'+response.xpath('//*[@id="breadcrumb"]/a[2]/text()').extract_first()+'>'+response.xpath('//*[@id="breadcrumb"]/a[3]/text()').extract_first()
        item["title"] = response.xpath("//*[@id='product_info']/div[1]/h1/@title").extract_first()
        item["detail"] = json.dumps(response.xpath("//*[@id='detail_describe']/ul//li/text()").extract(),ensure_ascii=False)
        item["link"] = response.url
        item["img_link"] =json.dumps(response.xpath("//div[@class='img_list']/ul//li/a/@data-imghref").extract())
        try:
            item["price"] = response.xpath("//*[@id='dd-price']/text()").extract()[1].strip()
        except IndexError as e:
            item["price"] = response.xpath("//*[@id='dd-price']/text()").extract()[0].strip()
        item["comment_num"] = response.xpath("//*[@id='comm_num_down']/text()").extract()[0]

        try:
            item["source"] = response.xpath("//*[@id='shop-geo-name']/text()").extract()[0].replace('\xa0至','')
        except IndexError as e:
            item["source"] = '当当自营'
        
        # 通过正则表达式提取url中的商品id
        goodsid = re.compile('\/(\d+).html').findall(response.url)[0]  
        commment_item['goods_id'] = goodsid
        item["goods_id"] = goodsid

        '''########################################################
                      通过抓包分析,提取商品的好评率             
        ########################################################'''
        # 提取详情页源码中的categoryPath
        script = response.xpath("/html/body/script[1]/text()").extract()[0]
        categoryPath = re.compile(r'.*categoryPath":"(.*?)","describeMap').findall(script)[0]
        # 构造包含好评率包的链接
        rate_url = "http://product.dangdang.com/index.php?r=comment%2Flist&productId="+str(goodsid)+"&categoryPath="+str(categoryPath)+"&mainProductId="+str(goodsid)
        r = requests.get(rate_url)
        data_dict = json.loads(r.text)
        item["rate"] = data_dict['data']['list']['summary']['goodRate']
        item["good_comment_num"] = data_dict['data']['list']['summary']['total_crazy_count']
        item["mid_comment_num"] = data_dict['data']['list']['summary']['total_indifferent_count']
        item["bad_comment_num"] = data_dict['data']['list']['summary']['total_detest_count']
        yield item

        '''#####################################################
                         开始对评论、评分进行清洗并爬取                 
        #####################################################'''
        html_str = data_dict['data']['list']['html']
        html = etree.HTML(html_str)
        comment_items = html.xpath('//div[@class="comment_items clearfix"]')
        pageIndex = 1
        while comment_items:   
            pageIndex += 1
            for item in comment_items:
                comment_unit = item.xpath('.//div[@class="describe_detail"][1]/span[not(@class="icon")]/text()')
                score = item.xpath('.//div[@class="pinglun"]/em/text()')[0]
                time = item.xpath('.//div[@class="items_right"]/div[@class="starline clearfix"][1]/span[1]/text()')[0]
                comment = ' '.join(comment_unit)
                commment_item["comment"] = comment 
                commment_item['score'] = score
                commment_item["time"] = time
                yield commment_item


            rate_url = "http://product.dangdang.com/index.php?r=comment%2Flist&productId="+str(goodsid)+"&categoryPath="+str(categoryPath)+"&mainProductId="+str(goodsid) + "&pageIndex=" + str(pageIndex)
            r = requests.get(rate_url)
            data_dict = json.loads(r.text)
            html_str = data_dict['data']['list']['html']
            html = etree.HTML(html_str)
            comment_items = html.xpath('//div[@class="comment_items clearfix"]')




