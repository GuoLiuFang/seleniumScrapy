import re
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
class CompanyInfoSpider(scrapy.Spider):
    name = "testdepth"
    page = 1
    start_urls = [
    'http://search.51job.com/list/010000,000000,0000,33,9,99,%25E9%2585%258D%25E4%25BB%25B6%252F%25E9%2594%2580%25E5%2594%25AE,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',
    ]   
    def parse(self, response):
        print('爬取的网页 URL 是%s' % response.url)
        print('当前是第%d 页' % self.page)
        next_page_list = response.css("li.bk a::attr(href)").extract()
        #这个网站永远不会有 None的，如果用 css 来进行提取的话
        whichpage = len(next_page_list)
        if whichpage == 1:
            if self.page == 1:
                next_page = next_page_list[0]
            else:
                next_page = None
        else:
            next_page = next_page_list[1]
        if next_page is not None:
            self.page = self.page + 1
            next_page = "http:" + next_page
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
