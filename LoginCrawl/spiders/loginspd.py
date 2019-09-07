# -*- coding: utf-8 -*-
import math

import requests
import scrapy
from scrapy import Request, FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
import urllib.request
import urllib.parse as urlparse
import cv2
import json
from Crypto.PublicKey import RSA
import execjs

from RsaSwust import encodePasswd


class LoginSpider(scrapy.Spider):
    # custom_settings = {
    #     'LOG_LEVEL': 'DEBUG',  # Log等级，默认是最低级别debug
    #     'ROBOTSTXT_OBEY': False,  # default Obey robots.txt rules
    #     'DOWNLOAD_DELAY': 2,  # 下载延时，默认是0
    #     'COOKIES_ENABLED': True,  # 默认enable，爬取登录后的数据时需要启用
    #     # 'COOKIES_DEBUG': True,      # 默认值为False,如果启用，Scrapy将记录所有在request(Cookie 请求头)发送的cookies及response接收到的cookies(Set-Cookie 接收头)。
    #     'DOWNLOAD_TIMEOUT': 20,  # 下载超时，既可以是爬虫全局统一控制，也可以在具体请求中填入到Request.meta中，Request.meta['download_timeout']
    #     'REDIRECT_ENALBED' : True
    # }

    name = 'loginspider'
    # allowed_domains = ['swust.edu.cn']
    # headers = {
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #     'Cache-Control': 'max-age=0',
    #     'Upgrade-Insecure-Requests': '1',
    #     'DNT': '1',
    #     'Accept-Encoding': 'gzip, deflate',
    #     'Accept-Language':'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
    #     'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    #     'Connection': 'keep-alive',
    # }

    start_urls = ['http://cas.swust.edu.cn/authserver/login?service=http%3a%2f%2fwww.gs.swust.edu.cn%2fsignin.aspx']

    def start_requests(self):
        """第一次请求一下登录页面，设置开启cookie使其得到cookie，设置回调函数"""
        return [Request('http://cas.swust.edu.cn/authserver/login?service=http%3a%2f%2fwww.gs.swust.edu.cn%2fsignin.aspx',
                        # cookies={'UM_distinctid':'169658745a9874-00017311f4431d-1333062-1fa400-169658745aa986'},
                        callback=self.parse)]

    def parse(self, response):
        # captcha = response.xpath("//html").extract()
        captcha = response.xpath("//img[@id='imgCode']//@src").extract()
        print(captcha)
        img_url = urlparse.urljoin(response.url, captcha[0])
        print(img_url)
        print('pls input the username')
        # username = input()
        username = "7020180384"
        print('pls input the passwd')
        # passwd = input()
        passwd = '19960809lsy'
        if len(captcha) > 0:
            print('the website has captcha')
            urllib.request.urlretrieve(img_url, filename='captcha.png')
            img = cv2.imread('captcha.png')
            cv2.imshow('image', img)
            cv2.waitKey(3000)
            cv2.destroyAllWindows()
            print('pls input the captcha')
            captcha = "dsadas"
            captcha = input()
            key_url = urlparse.urljoin(response.url, 'getKey')
            key_response = requests.get(key_url)
            item = key_response.json()
            encryptedpwd = encodePasswd(item['modulus'], item['exponent'], passwd)
            data = {
                'execution': response.xpath("//*[@ename='execution']/@value").extract(),
                '_eventId': response.xpath("//*[@ename='_eventId']/@value").extract(),
                'geolocation':response.xpath("//*[@geolocation='_eventId']/@value").extract(),
                'username': username,
                'password': encryptedpwd,
                'captcha': captcha,
                # 'redir':'www.gs.swust.edu.cn/Gstudent/Default.aspx',
                # 'redir': 'http://www.gs.swust.edu.cn/signin.aspx?ticket=ST-5199--xIcpf1Yr5GGVTrB4GSzlJyUklg-localhost',
                # 'redir': "http://cas.swust.edu.cn/authserver/login?service=http%3a%2f%2fwww.gs.swust.edu.cn%2fsignin.aspx"

            }
            print("login.......")
        else:
            print("none captcha")
        print(response)
        cookie = response.headers.getlist('Set-Cookie')
        return [FormRequest.from_response(response,
                                          formdata=data, callback=self.after_login, dont_filter=True)]
        # return [FormRequest.from_response(response, meta={"cookiejar": response.meta["cookiejar"]}, headers=self.header,
        #                                   formdata=data, callback=self.after_login)]

    def after_login(self, response):
        print(response.status)
        if authentication_failed(response):
            self.logger.error("Login failed")
            return


def authentication_failed(response):
    # TODO: Check the contents of the response and return True if it failed
    result = '//html'
    text = response.xpath(result).extract()
    print(text)
    xtitle = "/html/head/title/text()"
    text = response.xpath(xtitle).extract()
    print(text)
    result = '//*[@class="simLi"]/p/b/text()'
    text = response.xpath(result).extract()
    print(text)
    if len(text) >= 0:
        return False
    else:
        return True
