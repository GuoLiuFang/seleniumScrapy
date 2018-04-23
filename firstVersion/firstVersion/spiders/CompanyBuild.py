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
    name = "scrapebuildhr"
    pagemax = "p(?P<maxpage>\d+).html"
    def start_requests(self):
        #组合出来所有可能的 URL 抛出来
        for majorkey , majorvalue in CompanyCity.buildhr_major.items():
            for placekey, placevalue in CompanyCity.buildhr_citys.items():
                url = "http://www.buildhr.com/so/11-" + majorvalue + "-" + placevalue + ".html" 
                yield scrapy.Request(url, self.parse, meta={'majorkey':majorkey, 'placekey':placekey, 'current':1, 'maxpage':1})
    def parse(self, response):
        majorkey = response.meta['majorkey']
        placekey = response.meta['placekey']
        current = response.meta['current']
        maxpage = response.meta['maxpage']
        logging.log(logging.WARNING,"--------url-----%s------current---%d-------maxpage----%d--------majorkey---%s------placekey------%s------" % (response.url,current,maxpage,majorkey,placekey))
        filename = 'buildhr-%s-%s.log' % (CompanyCity.buildhr_major[majorkey], CompanyCity.buildhr_citys[placekey])
        with io.open(filename, 'a+', encoding='utf8') as f:
            for i in response.css("html body div.wrapper div.search_list div.list_middle table tr td.td_sp2 a::attr(href)").extract():
                page = "http://www.buildhr.com" + i
                if "vip.buildhr.com" in i or "top.buildhr.com" in i:
                    page = i.replace("http","").replace(":","").replace("//","")
                f.write(page + '\n')
        #先把当前页处理完成，再去解决下一页的问题
        maxpageurl = response.css("html body div.wrapper div.search_list div.list_bt div.common_bg2 a.a_icon05::attr(href)").extract_first()
        if maxpageurl is not None:
            matchresult = re.search(self.pagemax, maxpageurl)
            maxpage = int(matchresult.group("maxpage"))
        if current < maxpage:
            current = current + 1
            url = "http://www.buildhr.com/so/11-" + CompanyCity.buildhr_major[majorkey] + "-" + CompanyCity.buildhr_citys[placekey] + "-sm3-p" + str(current) + ".html"
            logging.log(logging.WARNING, "--------url-----%s------current---%d-------maxpage----%d" % (url,current,maxpage))
            yield scrapy.Request(url, self.parse, meta={'majorkey':majorkey, 'placekey':placekey, 'current':current, 'maxpage':maxpage})
