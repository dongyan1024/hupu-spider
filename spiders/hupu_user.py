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
        cookies = {'u': '29350540|5oiI5aOB54us54u8|bcc6|52e4b38e6d7ff1ccef9d90538cd9e8e0|6d7ff1ccef9d9053|aHVwdV8yMDMwNjY3ZThhNzRiNzgw', '__dacevst': '8d597d1a.8ebf6d3c|1532503097021', 'ua': '37378080', '_dacevid3': '44f3fb89.8f4c.4fcb.5f09.935e5f6df32d', '_cnzz_CV30020080': 'buzi_cookie%7C44f3fb89.8f4c.4fcb.5f09.935e5f6df32d%7C-1', '_CLT': '918ebe7bb324d8673460f7af1d701a5c', '_HUPUSSOID': 'a6d61dad-f441-4d7d-a1c8-8fc533ae7421', 'us': 'ea249c57c37f037e869deb60f0c43c02953e0482006908e7ae5d7fbe5825e73c0cdc912139590181f34413c9a6ab8966d40449da3801a1a6998d2f92c1721605', 'AUM': 'dgh5qNHqiWmf7EuJ5uhd1fbXjN5nt-yqlWtWpTno5j7lw'}

        yield scrapy.Request(self.base_urls, cookies=cookies, callback=self.parse_urls, dont_filter=True)

    def parse_urls(self, response):
        cookies = {
            'u': '29350540|5oiI5aOB54us54u8|bcc6|52e4b38e6d7ff1ccef9d90538cd9e8e0|6d7ff1ccef9d9053|aHVwdV8yMDMwNjY3ZThhNzRiNzgw',
            '__dacevst': '8d597d1a.8ebf6d3c|1532503097021', 'ua': '37378080',
            '_dacevid3': '44f3fb89.8f4c.4fcb.5f09.935e5f6df32d',
            '_cnzz_CV30020080': 'buzi_cookie%7C44f3fb89.8f4c.4fcb.5f09.935e5f6df32d%7C-1',
            '_CLT': '918ebe7bb324d8673460f7af1d701a5c', '_HUPUSSOID': 'a6d61dad-f441-4d7d-a1c8-8fc533ae7421',
            'us': 'ea249c57c37f037e869deb60f0c43c02953e0482006908e7ae5d7fbe5825e73c0cdc912139590181f34413c9a6ab8966d40449da3801a1a6998d2f92c1721605',
            'AUM': 'dgh5qNHqiWmf7EuJ5uhd1fbXjN5nt-yqlWtWpTno5j7lw'}
        for i in range(2, 102):
            url = '%s-%s' % (self.base_urls, i)
            yield scrapy.Request(url, cookies=cookies, callback=self.parse)

    def parse(self, response):

        article_address = LinkExtractor(restrict_css='a.truetit')
        for link in article_address.extract_links(response):
            yield scrapy.Request(link.url, meta={'cookiejar': 'chrome'}, callback=self.parse_detial)


    def parse_detial(self, response):

        user_address = LinkExtractor(restrict_css='div.left a.u')
        for link in user_address.extract_links(response):
            yield scrapy.Request(link.url, meta={'cookiejar': 'chrome'}, callback=self.parse_user, dont_filter=False)

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














