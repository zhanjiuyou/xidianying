# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import requests
import logging

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class DianyingSpiderMiddleware:
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

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
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


class DianyingDownloaderMiddleware:
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


class ProxyMiddleware():

    # 这块先改写from_crawler方法，给此类定义一个属性，将setting中得变量调用或者我们在上面声明setting都可以
    @classmethod
    def from_crawler(cls,crawler):
        settings = crawler.settings
        return cls(
            proxy_url = settings.get('PROXY_URL')
        )
    # 初始化变量，将settings文件中得变量导入过来调用
    def __init__(self,proxy_url):
        self.proxy_url = proxy_url
        self.logger = logging.getLogger(__name__)
    # 这里通过我们代理池搭建得api来获取代理
    def get_random_proxy(self):
        try:
            # 访问我们搭建得代理网页，获取代理。如果是本地项目调用代理得话我们只需使用本地得代理池，这块从网页获取api是为了分布式爬虫
            response = requests.get(self.proxy_url)
            # 如果网页正常响应200，则返回页面中得代理
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False

    # 该函数为执行函数，让爬虫下载时调用该函数
    def process_request(self,request,spider):
        # 当第一次访问没有反应得时候我们再尝试使用代理，如果正常可以访问则不使用代理，这里用到request得meta属性查看链接是否为重试链接
        if request.meta.get('retry_times'):
            proxy = self.get_random_proxy()
            # 获取到代理，如果有代理则执行
            if proxy:
                uri = 'http://{proxy}'.format(proxy=proxy)
                # 这里输出一个日志，来提醒流程正常运行
                self.logger.debug('使用代理'+ proxy)
                # 给request中属性添加代理
                request.meta['proxy'] = uri