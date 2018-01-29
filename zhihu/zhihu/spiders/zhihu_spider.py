# -*- coding: utf-8 -*-

from scrapy import Spider


class ZhihuSpider(Spider):
    name = 'zhihu'
    start_urls = [
        'https://www.zhihu.com/people/pi-pi-hui-ke-ting/activities'
    ]

    def __init__(self, *args, **kwargs):
        super(ZhihuSpider, self).__init__(*args, **kwargs)
