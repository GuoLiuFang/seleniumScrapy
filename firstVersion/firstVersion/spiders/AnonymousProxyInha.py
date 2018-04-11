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
start_urls = 'https://www.kuaidaili.com/free/inha/'
driver = webdriver.Firefox()
filename=sys.argv[0]
sep=sys.argv[1]
with io.open(filename, 'a+', encoding='utf8') as f:
    for page in range(1, sys.maxsize):
        try:
            driver.get(start_urls + str(page))
        except:
            print("当前访问页是%d" % page)
            sys.exit(0)
            os._exit(0)
        # 对每一页开始做操作。。。
        for tr in driver.find_elements_by_css_selector('table.table.table-bordered.table-striped tbody tr'):
            tds = tr.find_elements_by_css_selector("td")
            w = []
            w.append(tds[0].text)
            w.append(tds[1].text)
            w.append(tds[3].text)
            w.append(tds[4].text)
            w.append(tds[6].text)
            f.write(sep.join(w) + "\n")
            f.flush()