# 前言

本项目是基于scrapy框架的CrawlSpider类爬取当当全网商品信息，爬取的每条商品信息包括10个字段为：商品类别、商品名称、商品链接、商品价格、商品评论数、商品好评率、商品来源地、商品详情、商品图片链接。并将爬取的商品信息存储的mysql数据库中。

# 依赖

1. scrapy 1.5.0
2. python3.6
3. mysql 5.7
4. pymysql 库
5. scrapy-rotating-proxies 库
6. fake-useragent 库

# 使用方法

在命令行执行以下命令即可：

```bash
$ scrapy crawl dd
```

---

详细教程：[个人博客](https://runninggump.github.io/)