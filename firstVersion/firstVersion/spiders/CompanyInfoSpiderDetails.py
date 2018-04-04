import sys
import re
import os
sys.path.append(os.getcwd())
import CompanyCity
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
        whichplace = getattr(self, 'place', None)
        provincekey = CompanyCity.allprovince[whichplace] if whichplace in CompanyCity.allprovince else None
        citykey = CompanyCity.hotcitys[whichplace] if whichplace in CompanyCity.hotcitys else None
        if provincekey is None and citykey is None:
            print("请输入一下省份或者城市信息  '广东省' '江苏省' '浙江省' '四川省' '海南省' '福建省' '山东省' '江西省' '广西' '安徽省' '河北省' '河南省' '湖北省' '湖南省' '陕西省' '山西省' '黑龙江省' '辽宁省' '吉林省' '云南省' '贵州省' '甘肃省' '内蒙古' '宁夏' '西藏' '新疆' '青海省' '香港' '澳门' '台湾' '北京' '上海' '广州' '深圳' '武汉' '西安' '杭州' '南京' '成都' '重庆' '东莞' '大连' '沈阳' '苏州' '昆明' '长沙' '合肥' '宁波' '郑州' '天津' '青岛' '济南' '哈尔滨' '长春' '福州'   ") 
            os._exit(0)
        #filename = '51job-%s.log' % tag
        filename = '51job-%s-%s.log' % (tag, whichplace)
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                for line in f:
                    url = "http://" + line
                    print("读取文件获取链接%s" % url)
                    yield scrapy.Request(url, self.parse)
        else:
            print("文件%s 不存在！" % filename)
    def parse(self, response):
        print('当前处理的 URL 是%s' % response.url)
        self.log('当前处理的 URL 是%s' % response.url)
        yield {
                'tag':getattr(self, 'tag', None),
                'url':response.url,
                'whichplace':getattr(self, 'place', None),
                'company_name':re.sub('[\r\n \t]+','',response.css("div.in h1::attr(title)").extract_first().replace(u'\xa0','').replace('"','”') if response.css("div.in h1::attr(title)").extract_first() is not None else ''),
                'company_property':re.sub('[\r\n \t]+','',response.css("div.in p.ltype::text").extract_first().replace(u'\xa0','').replace('"','”') if response.css("div.in p.ltype::text").extract_first() is not None else ''),
                'company_selfintro':re.sub('[\r\n \t]+','',response.css("div.con_txt::text").extract_first().replace(u'\xa0','').replace('"','”') if response.css("div.con_txt::text").extract_first() is not None else ''),
                'company_address_label':re.sub('[\r\n \t]+','',response.css('p.fp span.label::text').extract_first().replace(u'\xa0','').replace('"','”') if response.css('p.fp span.label::text').extract_first() is not None else ''),
                'company_address_details':re.sub('[\r\n \t]+','',''.join(str(e) for e in response.css('p.fp::text').extract()).replace(u'\xa0','').replace('"','”') if response.css('p.fp::text').extract() is not None else ''),
                'company_website_label':re.sub('[\r\n \t]+','',response.css('p.fp.tmsg span.label::text').extract_first().replace(u'\xa0','').replace('"','”') if response.css('p.fp.tmsg span.label::text').extract_first() is not None else ''),
                'company_website_detials':re.sub('[\r\n \t]+','',response.css('p.fp.tmsg a::attr(href)').extract_first().replace(u'\xa0','').replace('"','”') if response.css('p.fp.tmsg a::attr(href)').extract_first() is not None else ''),
        }
