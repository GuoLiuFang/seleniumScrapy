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
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
import psycopg2
import psycopg2.extras
class JobDetailsSpider(scrapy.Spider):
    name = "jobDetails"
    page = 1
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
        dict_cur.execute("select id, url from batch.company_info_details where id >= %s and id <= %s" % (startid, stopid))
        resultall = dict_cur.fetchall()
        for url in resultall:
            yield scrapy.Request(url['url'].replace("%0A",""), callback=self.parse, meta={'CompanyID':url['id'], 'CompanyURL':url['url'].replace("%0A","")})

    def parse(self, response):
        CompanyID = response.meta['CompanyID']
        CompanyURL = response.meta['CompanyURL']
        #print('当前是第%d 页' % self.page)
        #print('当前id是%d' % id)
        #print('爬取的网页 URL 是%s' % CompanyURL)
        for x in response.css("div#joblistdata.dw_table div.el"):
            yield {
  	        'CompanyID':CompanyID,
	        'CompanyURL':CompanyURL,
	        'zw_name':x.css("p.t1 a.zw-name::text").extract_first(),
	        'zw_url':x.css("p.t1 a::attr(href)").extract_first(),
	        'zw_demand':x.css("span.t2::text").extract_first(),
	        'zw_location':x.css("span.t3::text").extract_first(),
	        'zw_salary':x.css("span.t4::text").extract_first(),
	        'zw_delivery_time':x.css("span.t5::text").extract_first(),
            }
        print("-----response.url----%s" % response.url)
        hidTotal = response.css("div#cpbotton.p_in ul input#hidTotal::attr(value)").extract_first()
        commit_url = "https:" + response.css("div#cpbotton.p_in ul input#hidAjax::attr(value)").extract_first()
        print("---------commit-url--------%s" % commit_url)
        maxpage = int(int(hidTotal) / 20) + 1
        print("maxpage---%d" % maxpage)
        while self.page < maxpage:
            self.page = self.page + 1
            print("------pageno------%d" % self.page)
            yield scrapy.FormRequest(url = commit_url, formdata = {'hidTotal':hidTotal, 'pageno':str(self.page),},  callback=self.parse, meta={'CompanyID':CompanyID, 'CompanyURL':CompanyURL})
