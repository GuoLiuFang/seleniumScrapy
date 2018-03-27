import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import scrapy
class CompanyInfoSpiderDetails(scrapy.Spider):
    name = "scrape51jobDetails"
    def start_requests(self):
        tag = getattr(self, 'tag', None)
        if tag is None:
            print("请输入要爬取的信息\n")
            os._exit(0)
        filename = '51job-%s.log' % tag
        with open(filename, 'r') as f:
            for line in f:
                url = "http://" + line
                print("读取文件获取链接%s" % url)
                yield scrapy.Request(url, self.parse)
    def parse(self, response):
        print('当前处理的 URL 是%s' % response.url)
        self.log('当前处理的 URL 是%s' % response.url)
        yield {
                'company_name':response.css("div.in h1::attr(title)").extract_first(),
                'company_property':response.css("div.in p.ltype::text").extract_first(),
                'company_selfintro':response.css("div.con_txt::text").extract_first(),
                'company_address_label':response.css('p.fp span.label::text').extract_first(),
                'company_address_details':response.css('p.fp::text').extract(),
                'company_website_label':response.css('p.fp.tmsg span.label::text').extract_first(),
                'company_website_detials':response.css('p.fp.tmsg a::attr(href)').extract_first(),
        }
