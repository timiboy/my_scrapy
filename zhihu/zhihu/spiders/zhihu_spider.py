# -*- coding: utf-8 -*-

from scrapy import Spider


class ZhihuSpider(Spider):

    def __init__(self, *args, **kwargs):
        super(ZhihuSpider, self).__init__(*args, **kwargs)
