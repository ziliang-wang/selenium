# 子良原创代码
import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class MyWebDriver:
    def __init__(self):
        self.driver = webdriver.PhantomJS()

    def crawl_job(self):
        url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,%2520,2,1.html'
        self.driver.get(url)
        if WebDriverWait(self.driver, 5, 0.5).until(
            EC.presence_of_element_located((By.ID, 'kwdselectid'))):
            kw = input('请输入要查询的主要技能: ')
            self.driver.find_element_by_id('kwdselectid').send_keys(kw)
            self.driver.find_element_by_class_name('p_but').click()
            if WebDriverWait(self.driver, 5, 0.5).until(
                EC.presence_of_element_located((By.ID, 'resultList'))):
                while True:
                    time.sleep(2)
                    self.__parse_data(self.driver.page_source)
                    try:
                        if self.driver.find_element_by_xpath('//li[@class="bk"][2]/a'):
                            self.driver.find_element_by_xpath('//li[@class="bk"][2]/a').click()
                    except:
                        break

    def __parse_data(self, page_source):
        html = etree.HTML(page_source)
        divs = html.xpath('//div[@id="resultList"]/div[@class="el"]')
        job_list = []
        for div in divs:
            job_dict = {}
            job_dict['title'] = div.xpath('./p/span/a/@title')[0]
            job_dict['company_name'] = div.xpath('./span[1]/a/@title')[0]
            job_dict['location'] = div.xpath('./span[2]/text()')[0]
            job_dict['salary'] = (div.xpath('./span[3]/text()')[0]
                                  if div.xpath('./span[3]/text()') else '无数据')
            job_dict['pub_date'] = div.xpath('./span[4]/text()')[0]
            job_list.append(job_dict)
            print(job_dict)


driver = MyWebDriver()
driver.crawl_job()