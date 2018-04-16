import io
import sys
import os
sys.path.append(os.getcwd())
import CompanyCity
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import scrapy
#增加在 Windows 下输出信息中文乱码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
import psycopg2
import psycopg2.extras
class ZwDetailsSpider(scrapy.Spider):
    name = "zwDetails"
    def start_requests(self):
        startid = getattr(self, 'startid', None)
        if startid is None:
            print("请输入开始 ID\n")
            sys.exit(0)
            os._exit(0)
        stopid = getattr(self, 'stopid', None)
        if stopid is None:
            print("请输入结束 ID\n")
            sys.exit(0)
            os._exit(0)
        hostarg = getattr(self, 'host', None)
        if hostarg is None:
            print("请输入结束 ID\n")
            sys.exit(0)
            os._exit(0)
        connection = psycopg2.connect(database="io", user="mdw", host=hostarg, port="5432", password="3edc$REW")
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        dict_cur.execute("select id, zw_url from batch.company_zw_details where id >= %d and id <= %d" % (startid, stopid))
        resultall = dict_cur.fetchall()
        for url in resultall:
            yield scrapy.Request(url['url'], callback=self.parse, meta={'JobID':url['id'], 'JobURL':rul['zw_url']})

    def parse(self, response):
        JobID = response.meta['JobID']
        JobURL = response.meta['JobURL']
        print('当前是第%d 页' % self.page)
        print('当前id是%d' % id)
        print('爬取的网页 URL 是%s' % JobURL)
        #zw_feature职位特色
        #zw_description职位描述
        zw_description = []
        for x in response.css("div.bmsg.job_msg.inbox p"):
            if x.css("::text").extract_first() is not None:
                zw_description.append(x.css("::text").extract_first())
        yield {
  	    'JobID':JobID,
	    'JobURL':JobURL,
            'zw_feature':re.sub('[\r\n \t]+','','|'.join(str(e) for e in response.css('div.jtag.inbox div.t1 span::text').extract()).replace(u'\xa0','').replace('"','”') if response.css('div.jtag.inbox div.t1 span::text').extract() is not None else ''),
	    'zw_welfare':re.sub('[\r\n \t]+','','|'.join(str(e) for e in response.css('div.jtag.inbox p.t2 span::text').extract()).replace(u'\xa0','').replace('"','”') if response.css('div.jtag.inbox p.t2 span::text').extract() is not None else ''),
	    'zw_description':'\n'.join(str(e) for e in zw_description)
	    'zw_location':re.sub('[\r\n \t]+','',''.join(str(e) for e in response.css('div.bmsg.inbox p.fp::text').extract()).replace(u'\xa0','').replace('"','”') if response.css('div.bmsg.inbox p.fp::text').extract() is not None else ''),
	    'zw_location':x.css("span.t3::text").extract_first(),
        }
