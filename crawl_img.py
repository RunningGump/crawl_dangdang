import pymysql
import json
import requests
import time
import urllib

# 连接数据库
db = pymysql.connect(host="localhost",user="root",passwd='******',db="dd",use_unicode=True, charset="utf8")
# 获取操作游标
cursor = db.cursor()
print('mysql connet success!')

# SQL查询语句
sql = "SELECT * FROM goods"

try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取一条记录列表
    results = cursor.fetchall()
    for row in results:
        img_links = json.loads(row[-1])
        goods_id = row[0]
        for img_link in img_links:
            img_path = './goods_img/' + str(goods_id) + '_{0}.jpg'.format(int(time.time()*100))
            urllib.request.urlretrieve(img_link, img_path)

except:
    print('Error: unable to fetch data')

# 关闭数据库连接
db.close()
