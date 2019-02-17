# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from weixin import settings

class WeixinPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host = settings.MYSQL_HOST,
            port = settings.MYSQL_PORT,
            db = settings.MYSQL_DBNAME,
            user = settings.MYSQL_USER,
            passwd = settings.MYSQL_PASSWORD,
            charset = 'utf8',
            use_unicode = True )
        self.cursor = self.connect.cursor()

    # 数据入库方法
    def insertData(self, item):
        sql = "insert into article(article_title, article_urlx, writer, intro, article_urly) VALUES(%s, %s, %s, %s, %s);"
        params = (item['article_title'], item['article_urlx'], item['writer'], item['intro'], item['article_urly'])
        self.cursor.execute(sql, params)
        self.connect.commit()

    # 数据清洗方法
    def cls(self, item):
        article_title_cls = item['article_title']
        if article_title_cls:
            item['article_title'] = article_title_cls.strip().replace('\n','').replace(' ','').replace('None','')

        article_urlx_cls = item['article_urlx']
        if article_urlx_cls:
            item['article_urlx'] = article_urlx_cls.strip().replace('\n','').replace(' ','')

        writer_cls = item['writer']
        if writer_cls:
            item['writer'] = writer_cls.strip().replace('\n','').replace(' ','')

        intro_cls = item['intro']
        if intro_cls:
            item['intro'] = intro_cls.strip().replace('\n','').replace(' ','')

        article_urly_cls = item['article_urly']
        if article_urly_cls:
            item['article_urly'] = article_urly_cls.strip().replace('\n','').replace(' ','')

    def process_item(self, item, spider):
        self.cls(item)
        self.insertData(item)
        return item
