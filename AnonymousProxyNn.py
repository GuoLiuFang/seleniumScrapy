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
#因为 scrapy 禁止抓取所以使用 selenium 进行抓取
driver = webdriver.Firefox()
start_urls = "http://www.xicidaili.com/nn/"
for page in range(1, sys.maxsize):
    try:
        driver.get(start_urls + str(page))
    except:
        print("当前访问页是%d" % page)
        sys.exit(0)
        os._exit(0)
    x = driver.find_elements_by_css_selector("table#ip_list tbody tr.odd")
    filename=sys.argv[0]
    sep=sys.argv[1]
    with io.open(filename, 'a+', encoding='utf8') as f:
        for z in x:
            y = z.find_elements_by_css_selector("td")
            w = []
            w.append(y[1].text)
            w.append(y[2].text)
            w.append(y[5].text)
            w.append(y[3].text)
            w.append(y[9].text)
            f.write(sep.join(w) + "\n")
            f.flush()
