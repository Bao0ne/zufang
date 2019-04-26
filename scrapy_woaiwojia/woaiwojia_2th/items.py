# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ErshoufangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #block = scrapy.Field()
    title = scrapy.Field()  # 标题
    href = scrapy.Field()  # 详情链接
    area = scrapy.Field()   #区域
    metro = scrapy.Field()   #地铁(is)
    price = scrapy.Field()  # 价格
    h_method = scrapy.Field()   #出租方式
    square = scrapy.Field()   #面积
    huxing = scrapy.Field()   #户型
    orientation = scrapy.Field()   #朝向
    floor = scrapy.Field()   #楼层
    renovation = scrapy.Field()   #装修(is)
    view = scrapy.Field()   #近30天看房次数
    time = scrapy.Field()   #发布时间
    tags = scrapy.Field()   #标签


