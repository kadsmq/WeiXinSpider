# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeixinItem(scrapy.Item):
    # define the fields for your item here like:

    article_title = scrapy.Field()  # 文章标题
    article_urlx = scrapy.Field()   # 文章详情页URL
    writer = scrapy.Field()         # 文章作者
    intro = scrapy.Field()          # 文章简介
    article_urly = scrapy.Field()   # 读取阅读原文的URL地址
