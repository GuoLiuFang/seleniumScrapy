# -*- coding: utf-8 -*-

# Scrapy settings for firstVersion project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
FEED_EXPORT_ENCODING = 'utf-8'
BOT_NAME = 'firstVersion'

SPIDER_MODULES = ['firstVersion.spiders']
NEWSPIDER_MODULE = 'firstVersion.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'firstVersion (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
#ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'firstVersion.middlewares.FirstversionSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'firstVersion.middlewares.MyCustomDownloaderMiddleware': 543,
}
#在这里设置 userAgent 和 proxy,在这里进行全量加载
#ssh -L 13306:10.127.84.14:13306 ws1
import pymysql
import os
import sys
sys.path.append(os.getcwd())
connection = pymysql.connect(host='localhost',port=13306,user='webuser',password='123.c0m',db='lk',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
PROXIES = []
try:
    with connection.cursor() as cursor:
        sql = "select * from `anonymous_proxy` limit 10"
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in result:
            # to_list.append(str(i['email']))
            # print("ip----%s" % i['ip'])
            # print("port----%d" % i['port'])
            # print("type----%s" % i['type'])
            # print("location----%s" % i['location'])
            # print("verify_time----%s" % i['verify_time'])
            # print(i['type'].lower()+"://" + i['ip'] + ":" + str(i['port']))
            PROXIES.append(i['type'].lower()+"://" + i['ip'] + ":" + str(i['port']))
except:
    print("获取数据出现异常")
    sys.exit(0)
    os._exit(0)
# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'firstVersion.pipelines.FirstversionPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
DUPEFILTER_DEBUG = True
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
