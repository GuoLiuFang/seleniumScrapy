import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import scrapy
class CompanyInfoSpider(scrapy.Spider):
    name = "scrape51job"
    def start_requests(self):
        tag = getattr(self, 'tag', None)
        if tag is None:
            print("请输入要爬取的信息\n")
            os._exit(0)
        driver = webdriver.Firefox()
        driver.get("http://www.51job.com")
        assert "招聘" in driver.title
        elem = driver.find_element_by_id("kwdselectid")
        elem.clear()
        elem.send_keys(tag)
        elem.send_keys(Keys.RETURN)
        try:
            WebDriverWait(driver, 10).until(EC.title_contains(tag))
        finally:
            print("页面没有加载完成，超时了")
        url = driver.current_url
        print('动态生成的网页 URL 是%s' % url)
        driver.close()
        yield scrapy.Request(url, self.parse)
    def parse(self, response):
        tag = getattr(self, 'tag', None)
        print('爬取的网页 URL 是%s' % response.url)
        for i in response.css("span.t2 a::attr(href)").extract():
            page = i.split("//")[-1]
            #yield {
            #        'companyurl' : page
            #}
            filename = '51job-%s.log' % tag
            with open(filename, 'a+') as f:
                f.write(page + '\n')
        next_page = "http:" + response.css("li.bk a::attr(href)").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
