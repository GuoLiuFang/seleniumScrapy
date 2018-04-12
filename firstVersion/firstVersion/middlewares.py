# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
#import pymysql
#import os
#import io
#import sys
#connection = pymysql.connect(host='localhost',port=13306,user='webuser',password='123.c0m',db='lk',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
PROXIES = []
#current_ip = ''
#try:
#    with connection.cursor() as cursor:
#        sql = "select * from `anonymous_proxy` where net_speed < 1 and connect_speed < 1"
#        cursor.execute(sql)
#        result = cursor.fetchall()
#        for i in result:
#            # to_list.append(str(i['email']))
#            # print("ip----%s" % i['ip'])
#            # print("port----%d" % i['port'])
#            # print("type----%s" % i['type'])
#            # print("location----%s" % i['location'])
#            # print("verify_time----%s" % i['verify_time'])
#            # print(i['type'].lower()+"://" + i['ip'] + ":" + str(i['port']))
#            PROXIES.append(i['type'].lower()+"://" + i['ip'] + ":" + str(i['port']))
#except:
#    print("获取数据出现异常")
#    sys.exit(0)
#    os._exit(0)
import random
class MyCustomDownloaderMiddleware(object):
    #@classmethod
    #def from_crawler(cls, crawler):

    # 在这里完成代理的事情。。每一个 request 重新非一个代理。。
    def process_request(self, request, spider):
        #通过setting获取 MySQL，因为 setting 只被执行一次。。
        #proxy = "http://220.184.33.129:9000"
        #proxy = "https://218.72.111.103:18118"
        proxy = random.choice(PROXIES)
        #current_ip = proxy
        #在这里处理，异常消费的问题
        print("本次请求%s的代理 ip 地址为%s" % (request,proxy))
        request.meta['proxy'] = proxy
        #request.meta['max_retry_times'] = 1
    def process_exception(self, request, exception, spider):
        print("**捕获到异常**")
        print(str(exception))
        #把当前 ip写入到黑名单中去。。
        #with io.open('black_list.txt','a+',encoding='utf8') as f:
        #    f.write(current_ip + '\n')
        #    f.flush()
        print("**捕获到异常**")



class FirstversionSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
