# 前言

本项目是基于scrapy框架的CrawlSpider类爬取当当全网商品信息，爬取的每条**商品信息**包括13个字段为：商品id、商品类别、商品名称、商品价格、评论数量、好评数、中评数、差评数、好评率、商品来源、商品详情、商品连接、商品图片连接。以及**评论信息**包括4个字段：商品id、评论、商品评分、评论时间。并将爬取的商品信息存储的mysql数据库中goods数据表中，将评论信息存储的comments数据表中。

# 依赖

1. scrapy 1.5.0
2. python3.6
3. mysql 5.7.24
4. pymysql 库
5. scrapy-rotating-proxies 库
6. fake-useragent 库

# 使用方法

1. 创建数据库名为dd，并在数据库dd下创建两个数据表goods、comments。

2. 将程序中的数据库用户名和密码改成自己的。

3. 在命令行执行以下命令即可：

```bash
$ scrapy crawl dd
```

---

详细教程：[个人博客](https://runninggump.github.io/2018/09/01/%E5%9F%BA%E4%BA%8EScrapy%E6%A1%86%E6%9E%B6%E7%9A%84CrawlSpider%E7%B1%BB%E7%88%AC%E5%8F%96%E5%BD%93%E5%BD%93%E5%85%A8%E7%BD%91%E5%95%86%E5%93%81%E4%BF%A1%E6%81%AF/)