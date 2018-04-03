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
    name = "scrape51job"
    page = 1
    def start_requests(self):
        tag = getattr(self, 'tag', None)
        if tag is None:
            print("请输入要爬取的信息\n")
            os._exit(0)
        driver = webdriver.Firefox()
        driver.get("http://www.51job.com")
        assert "招聘" in driver.title
        whichplace = getattr(self, 'place', None)
        provincekey = CompanyCity.allprovince[whichplace] if whichplace in CompanyCity.allprovince else None
        citykey = CompanyCity.hotcitys[whichplace] if whichplace in CompanyCity.hotcitys else None
        if provincekey is None and citykey is None:
            print("请输入一下省份或者城市信息  '广东省' '江苏省' '浙江省' '四川省' '海南省' '福建省' '山东省' '江西省' '广西' '安徽省' '河北省' '河南省' '湖北省' '湖南省' '陕西省' '山西省' '黑龙江省' '辽宁省' '吉林省' '云南省' '贵州省' '甘肃省' '内蒙古' '宁夏' '西藏' '新疆' '青海省' '香港' '澳门' '台湾' '北京' '上海' '广州' '深圳' '武汉' '西安' '杭州' '南京' '成都' '重庆' '东莞' '大连' '沈阳' '苏州' '昆明' '长沙' '合肥' '宁波' '郑州' '天津' '青岛' '济南' '哈尔滨' '长春' '福州'   ") 
            os._exit(0)
        #先选择地区，搞错了抱歉
        addbut = driver.find_element_by_css_selector('p#work_position_click.addbut')
        addbut.click()
        #取消地区选项
        cancelCity = driver.find_element_by_css_selector('span#work_position_click_multiple_selected_each_010000.ttag')
        cancelCity.click()
        placekey = citykey
        if provincekey is not None:
            placekey = provincekey
            eleprovince = driver.find_element_by_css_selector('li#work_position_click_center_left_each_030000')
            eleprovince.click()
        #勾选参数选定的地区
        addCity = driver.find_element_by_css_selector(placekey)
        addCity.click()
        #点击确定键
        sureadd = driver.find_element_by_css_selector('span#work_position_click_bottom_save.p_but')
        sureadd.click()
        #输入搜索的专业内容
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
        whichplace = getattr(self, 'place', None)
        print('当前是第%d 页' % self.page)
        print('爬取的网页 URL 是%s' % response.url)
        for i in response.css("span.t2 a::attr(href)").extract():
            page = i.split("//")[-1]
            #yield {
            #        'companyurl' : page
            #}
            filename = '51job-%s-%s.log' % (tag, whichplace)
            with open(filename, 'a+') as f:
                f.write(page + '\n')
        next_page_list = response.css("li.bk a::attr(href)").extract()
        #这个网站永远不会有 None的，如果用 css 来进行提取的话
        whichpage = len(next_page_list)
        if whichpage == 1:
            if self.page == 1:
                next_page = next_page_list[0]
                print("这个页面%s是开始页" % response.url)
            else:
                next_page = None
                print("这个页面%s是结束页" % response.url)
        elif whichpage > 1:
            next_page = next_page_list[1]
        else:
            print("这个页面%s上一页和下一页按钮不可用" % response.url)
            next_page = None
        if next_page is not None:
            self.page = self.page + 1
            #print("未加 http 之前:" + next_page)
            #next_page = "http:" + next_page
            #print("加了 http 之后:" + next_page)
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
