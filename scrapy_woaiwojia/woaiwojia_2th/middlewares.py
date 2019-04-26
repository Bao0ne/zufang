# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging
import random
import requests

class RandomUserAgentMiddleware():
    def __init__(self, user_agent_list):
        self.user_agent_list = user_agent_list
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            crawler.settings.get('USER_AGENT_LIST')
        )

    def process_request(self, request, spider):
        rand_use = random.choice(self.user_agent_list)
        request.headers['User-Agent'] = rand_use
        #self.logger.debug('使用随机User-Agent\n{}'.format(request.headers['User-Agent']))
        return None


class ProxyMiddleware():
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            crawler.settings.get('PROXY_URL')
        )

    def get_random_proxy(self):
        try:
            r = requests.get(self.proxy_url)
            if r.status_code == 200:
                proxy = r.text
                #self.logger.debug('获得代理 {}'.format(proxy))
                return proxy
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        #默认使用代理，重试才会用本机ip
        retry_times = request.meta.get('retry_times')
        if not retry_times or retry_times < 2:
            proxy = self.get_random_proxy()
            #proxy = '1.1.1.1:1111'
            ip = proxy.split(':')[0]
            if proxy :
                uri = 'http://{}'.format(proxy)
                request.meta['proxy'] = uri
                self.logger.debug('使用代理<{}>请求{}'.format(request.meta['proxy'], request.url))
            else:
                #这里可以自定义error并raise
                self.logger.error('获取代理失败！')
                self.get_random_proxy()
                print('重试')
        else:
            #清除之前设置的代理，默认使用本机ip
            request.meta['proxy'] = None
            #self.logger.debug('使用本机请求{}'.format(request.url))
        return None



class Woaiwojia2ThSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Woaiwojia2ThDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
