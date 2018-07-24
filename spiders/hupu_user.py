# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import browsercookie
from scrapy.linkextractors import LinkExtractor

from ..items import HupuItem

class HupuUserSpider(scrapy.Spider):
    name = 'hu'
    #allowed_domains = ['hupu.com']
    base_urls = 'http://bbs.hupu.com/bxj'

    def start_requests(self):
        yield scrapy.Request(self.base_urls, callback=self.parse_urls, dont_filter=True)

    def parse_urls(self, response):
        for i in range(2, 102):
            url = '%s-%s' % (self.base_urls, i)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        article_address = LinkExtractor(restrict_css='a.truetit')
        for link in article_address.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_detial)


    def parse_detial(self, response):
        user_address = LinkExtractor(restrict_css='div.left a.u')
        for link in user_address.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_user, dont_filter=False)

    def parse_user(self, response):
        user = HupuItem()
        select = response.css('div.personal')
        user['name'] = select.xpath('./div/h3/div/text()').extract_first()
        user['quantity'] = select.xpath('./div/h3/span/text()').re_first('\d+')
        user['gender'] = select.xpath('//span[@itemprop="gender"]/text() '). extract_first()
        user['home'] = select.xpath('//span[@itemprop="address"]/text() '). extract_first()
        user['prestige'] = select.xpath('//span[contains(./text(), "社区声望" )]/following:: text()[1]'). re_first('\d+')
        user['level'] = select.xpath('//span[contains(./text(), "社区等级" )]/following:: text()[1]'). re_first('\d+')
        user['online_time'] = select.xpath('//span[contains(./text(), "在线时间" )]/following:: text()[1]'). re_first('\d+')
        user['register_time'] = select.xpath('//span[contains(./text(), "加入时间" )]/following:: text()[1]'). re_first('\d{4}-\d{2}-\d{2}')
        yield user














