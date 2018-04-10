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
    name = "anonymousproxyInha"
    page = 1
    start_urls = [
    'https://www.kuaidaili.com/free/inha/',
    ]
    def parse(self, response):
        print('当前是第%d 页' % self.page)
        print('爬取的网页 URL 是%s' % response.url)
        for tr in response.css('table.table.table-bordered.table-striped tbody tr'):
            yield {
                    'ip':tr.css("td::text").extract()[0],
                    'port':tr.css("td::text").extract()[1],
                    'type':tr.css("td::text").extract()[3],
                    'location':tr.css("td::text").extract()[4],
                    'verify_time':tr.css("td::text").extract()[6],
            }
        self.page = self.page + 1
        next_page = self.start_urls[0] + self.page
        next_page = response.urljoin(next_page)
        yield scrapy.Request(next_page, callback=self.parse)
