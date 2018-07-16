# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HupuItem(scrapy.Item):
    #标题
    #title = scrapy.Field()
    #用户名
    name = scrapy.Field()
    #访问量
    quantity = scrapy.Field()
    #性别
    gender = scrapy.Field()
    #所在地
    home = scrapy.Field()
    #声望
    prestige = scrapy.Field()
    #论坛等级
    level = scrapy.Field()
    #在线时长
    online_time = scrapy.Field()
    #注册时间
    register_time = scrapy.Field()

