# -*- coding: utf-8 -*-

# 实现登陆并存储cookies以方便后续进行数据抓取
import requests
import json
import re
from datetime import datetime, timedelta
import time
from hashlib import sha1
import hmac
from requests_toolbelt import MultipartEncoder

# 账户列表， 为防止对爬虫的限制， 一般来说需要多个帐号
ZHIHU_ACCOUNT = [
    {'username':'123', 'password':'123'},
    # {'username':'2', 'password':'2'},
]


# 基础headers
BASE_HEADERS = {
            "Origin": "https://www.zhihu.com",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "X-Xsrftoken": '',
            "X-UDID": '',
            "Connection": "keep-alive",
            "accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Host": "www.zhihu.com",
            "Referer": "https://www.zhihu.com/signup?next=%2F",
            "authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"  # 注意这里在js文件中时固定的一个字串
        }

class ZhihuLogin():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.headers = BASE_HEADERS.copy()
        self.formdata = ''

    def _prelogin(self):
        # 知乎在登陆网页时有set cookies步骤, 所以需要有预登陆, 并且通过这一步获取登陆需要的其它一些数据
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        url = 'https://www.zhihu.com/signup?next=//'
        resp = self.session.get(url, headers=headers)
        if resp.status_code != 200:
            return False
        return resp.text

    def _get_auth_data(self, text):
        # 从登陆页面中提取出 xsrf 和 udid
        xsrf_regex = re.compile(r'&quot;xsrf&quot;:&quot;(.+?)&quot;')
        udid_regex = re.compile(r'xUDID&quot;:&quot;(.+?)&quot;')
        xsrf = xsrf_regex.search(text).group(1)
        udid = udid_regex.search(text).group(1)
        return xsrf, udid

    def _set_headers(self):
        # 设置headers的值
        text = self._prelogin()
        xsrf, udid = self._get_auth_data(text)
        self.headers['X-Xsrftoken'] = xsrf
        self.headers['X-UDID'] = udid
        self.udid = udid

    def _get_timestamp(self):
        return str(long(time.time() * 1000))

    def _get_signature(self, timestamp):
        hashed = hmac.new('d1b964811afb40118a12068ff74a12f4', '', sha1)
        hashed.update('password')
        hashed.update('c3cef7c66a1843f8b3a9e6a1e3160e20')
        hashed.update('com.zhihu.web')
        hashed.update(timestamp)
        return hashed.hexdigest()

    def _get_formdata(self):
        timestamp = self._get_timestamp()
        data = {
            "username": "+86%s" % self.username,
            "lang": "en",
            "password": self.password,
            "captcha": "",
            "timestamp": timestamp,
            "utm_source": "",
            "source": "com.zhihu.web",
            "ref_source": "homepage",
            "client_id": "c3cef7c66a1843f8b3a9e6a1e3160e20",
            "signature": self._get_signature(timestamp),
            "grant_type": "password"
        }
        return data

    def _format_formdata(self, data, boundary='----WebKitFormBoundarypgm1aPMShIA9io9c'):
        encoder = MultipartEncoder(fields=data, boundary=boundary)
        self.headers['Content-type'] = encoder.content_type
        return encoder.to_string()

    def _login(self):
        self._set_headers()
        url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
        formdata = self._get_formdata()
        self.formdata = self._format_formdata(data=formdata)
        retry = True
        while retry:
            resp = self.session.get('https://www.zhihu.com/api/v3/oauth/captcha?lang=en', headers=self.headers) # 正式登陆前用相同的请求头访问验证码接口
            print resp.text
            if not json.loads(resp.text).get('show_captcha', True):
                retry = False
            time.sleep(0.5)
        resp = self.session.post(url, headers=self.headers, data=self.formdata)
        print resp.text


    def get_cookies(self):
        self._login()
        self.cookies = self.session.cookies.get_dict()
        self.zc_0 = self.cookies.get('z_c0')

def get_cookies():
    cookies = []
    for each in ZHIHU_ACCOUNT:
        username = each.get('username')
        password = each.get('password')
        l = ZhihuLogin(username, password)
        l.get_cookies()
        cookies.append(l)
    return cookies


COOKIES_LIST = get_cookies()

if __name__ == '__main__':
    pass
