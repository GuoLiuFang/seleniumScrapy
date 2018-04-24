import logging
import re
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
class CompanyInfoSpider(scrapy.Spider):
    name = "scrapebuildhrCompany"
    def start_requests(self):
        #组合出来所有可能的 URL 抛出来
        for majorkey , majorvalue in CompanyCity.buildhr_major.items():
            for placekey, placevalue in CompanyCity.buildhr_citys.items():
                filename = 'buildhr-%s-%s.log' % (CompanyCity.buildhr_major[majorkey], CompanyCity.buildhr_citys[placekey])
                with io.open(filename, 'r', encoding='utf8') as f:
                    for url in f:
                        if "vip.buildhr.com" in url:
                            logging.warning("这是 VIP 的网页，暂时先不解析--url---%s----" % url)
                        elif "top.buildhr.com" in url:
                            url = "http://" + url
                        else:
                            pass
                        yield scrapy.Request(url.replace("%0A",""), self.parse, meta={'majorkey':majorkey, 'placekey':placekey, })
    def parse(self, response):
        majorkey = response.meta['majorkey']
        placekey = response.meta['placekey']
        #公司简介拿下：
        companyselfinfo = response.css("html body div.wrapper div.wrap_lt.wrap_no div.wrap_lt.com_info div.company_contact.company_contact_mb.u_whsn p font::text").extract()
        if len(companyselfinfo) == 0:
            companyselfinfo = response.css("div.wrap_lt.wrap_no div.wrap_lt.com_info div.company_contact.company_contact_mb.u_whsn p::text").extract()
        #公司属性拿下
        a = response.css("div.wrap_lt.wrap_no div.wrap_lt.com_info div.c_lf ul.company_info li span::text").extract()
        b = response.css("div.wrap_lt.wrap_no div.wrap_lt.com_info div.c_lf ul.company_info li::text").extract()
        m = dict(zip(a,b))
        company_property = str(m)
        b = response.css("div.wrap_lt.wrap_no div.wrap_lt.com_info div.company_contact.company_contact_mb ul li::text").extract()
        a = response.css("div.wrap_lt.wrap_no div.wrap_lt.com_info div.company_contact.company_contact_mb ul li strong::text").extract()
        m = dict(zip(a,b))
        company_contact = str(m)
        a = response.css("div.company_contact.company_contact_mb.company_beian ul.clearfix li span.title::text").extract()
        b = response.css("div.company_contact.company_contact_mb.company_beian ul.clearfix li span.value::text").extract()
        m = dict(zip(a,b))
        company_credit = str(m)
        yield {
            "major":majorkey,
            "whichplace":placekey,
            "url":response.url.replace("%0A",""),
            "companyname":response.css("div.wrap_lt.com_info div.c_lf h1.h2_sp.bt::text").extract_first(),
            "companyselfinfo":re.sub('[\r\n \t]+','',''.join(companyselfinfo).replace("\u3000","").replace(u'\xa0','').replace('"','”')).replace('：',''),
            "company_property":re.sub('[\r\n \t]+','',''.join(company_property).replace("\u3000","").replace(u'\xa0','').replace('"','”')).replace('：',''),
            "company_contact":re.sub('[\r\n \t]+','',''.join(company_contact).replace("\u3000","").replace(u'\xa0','').replace('"','”')).replace('：',''),
            "company_credit":re.sub('[\r\n \t]+','',''.join(company_credit).replace("\u3000","").replace(u'\xa0','').replace('"','”')).replace('：',''),
        }
