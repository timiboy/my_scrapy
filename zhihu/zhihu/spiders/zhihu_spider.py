# -*- coding: utf-8 -*-
import re
import random
import json
import time

from scrapy import Spider
from scrapy.http import Request, Response

from ..utils.get_cookies import COOKIES_LIST
from ..utils.database import mongo_handler


class ZhihuSpider(Spider):
    name = 'zhihu'
    start_urls = [
        'https://www.zhihu.com/people/meng-meng-da-meng-meng-da-meng-meng-da/activities'
    ]
    cookie = random.choice(COOKIES_LIST)
    profile_url = 'https://www.zhihu.com/api/v4/members/%s?include=allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'
    following_url = 'https://www.zhihu.com/api/v4/members/%s/followees?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset=120&limit=20'

    def __init__(self, *args, **kwargs):
        super(ZhihuSpider, self).__init__(*args, **kwargs)
        self.username_set = set()
        self.headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Connection':'keep-alive',
            'Host':'www.zhihu.com',
            'X-UDID':self.cookie.udid,
            'authorization':'Bearer %s' % self.cookie.zc_0
        }

    def parse(self, response):
        username = response.url.split('/')[4]
        print '----------------------------'
        print username
        print '----------------------------'
        return Request(self.profile_url % username, callback=self.profile_parse, headers=self.headers, \
                       cookies=self.cookie.cookies, meta={'username':username})

    def profile_parse(self, response):
        profile = response.body
        username = response.meta['username']
        self.username_set.add(username)
        mongo_handler.db.zhihu_profile.update({'url_token':username}, json.loads(profile), True, True)
        return Request(self.following_url % username, callback=self.following_parse, headers=self.headers, \
                       cookies=self.cookie.cookies)

    def following_parse(self, response):
        users = json.loads(response.body)
        for each in users.get('data', []):
            time.sleep(0.5)
            username = each.get('url_token', '')
            if username and username not in self.username_set:
                yield Request(self.profile_url % username, callback=self.profile_parse, headers=self.headers, \
                              cookies=self.cookie.cookies, meta={'username':username})
        if not users.get('paging', {}).get('is_end', True):
            print '==============================='
            print u'下一个'
            print '==============================='
            next_page = users.get('paging', {}).get('next', '')
            yield Request(next_page, callback=self.following_parse, headers=self.headers, cookies=self.cookie.cookies)
