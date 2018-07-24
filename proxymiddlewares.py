# -*- coding: utf-8 -*-
import random, base64


class ProxyMiddleware(object):
    proxyList = [
        '140.143.62.87:8888', '47.96.82.230:8888',
    ]

    def process_request(self, request, spider):
        # Set the location of the proxy
        pro_adr = random.choice(self.proxyList)
        print("USE PROXY -> " + pro_adr)
        request.meta['proxy'] = "http://" + pro_adr