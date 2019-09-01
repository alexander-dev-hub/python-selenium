# -*- coding: utf-8 -*-
#
# Created by: https://github.com/Hopetree
#
# Created data: 2017/7/29

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import datetime
from lxml import etree
import codecs

import json
import re


Chromedriver = webdriver.Chrome(executable_path = r'E:\tool\chromedriver_win32\chromedriver.exe')
BASE_URL= 'https://shop.vons.com/'
HOME_URL= 'https://shop.vons.com/home.html'
PFILE="shop_vons.json"
class ShopvonsCrawler(object):
    def __init__(self):
        '''Check double add product'''
        self.set = set()
       
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"}
        
        self.base_url = BASE_URL

        self.file = codecs.open(PFILE, 'w', encoding='utf-8')
        self.zipcode='90042'
        self.driver = Chromedriver
        self.waiter = WebDriverWait(self.driver,5)
        #self.driver.maximize_window()
        self.driver.get(HOME_URL)
        time.sleep(0.2)
        self.driver.find_element_by_id("zipcode").clear()
        self.driver.find_element_by_id("zipcode").send_keys(self.zipcode)
        btnsubmit= self.driver.find_element_by_css_selector('input[class="btn btn-default"]')
        btnsubmit.click()

    def save_info(self, name, link):
        
        url = BASE_URL+link 
        print(name, url)
        item = {name: url}
        line = json.dumps(item, ensure_ascii=False) + "\n"
        self.file.write(line)

    def getall(self):
        #wait home page load
        time.sleep(10)
        
        
        try:
            #get all category after home load
            self.waiter.until(
                EC.presence_of_element_located((By.XPATH,'//div[contains(@class,"product-carousel aem-GridColumn aem-GridColumn--default--12")]'))
            )
            tree = etree.HTML(self.driver.page_source)
            categories = tree.xpath('//div[contains(@class,"product-carousel aem-GridColumn aem-GridColumn--default--12")]')
            for category in categories:
                #/html/body/div[1]/div/div/div[2]/div/div[3]/div[1]/div/h2
                #div= category.xpath('text()').extract_first()
                catname = category.xpath('div/div/h2/text()')[0]
                caturl = category.xpath('div/div/div/a[@class="view-link"]/@href')[0]
                if caturl:
                    print (catname, caturl)
                    self.get_category(catname, caturl)
                    
                    
                    #catlinks = self.driver.find_elements_by_css_selector("a[class='view-link']")  
     
        except TimeoutException as e:
            print(e)
        finally:
            self.file.close()    
    def get_category(self,catname, caturl):
        
        self.driver.get(BASE_URL+caturl)     
        #self.sheet = self.wk.add_sheet(catname)
        time.sleep(5)

        caturl = self.driver.current_url
        print(caturl)
        products = self.waiter.until(
                EC.presence_of_element_located((By.XPATH,'//product-generic-grid//product-item'))
        )
        tree = etree.HTML(self.driver.page_source)
        products = tree.xpath('//product-generic-grid//product-item')
           
        for p in products:

            pname= p.xpath('.//h3/a[@class="product-title"]/text()')
            if pname:
                pname= pname[0].strip()
            plink= p.xpath('.//h3/a[@class="product-title"]/@href') 
            if plink:    
                plink=plink[0]
            
            if plink not in self.set:
                try:
                    self.save_info(pname, plink)
                    self.set.add(plink)
                except Exception as e:
                        print(pname, e)

if __name__ == '__main__':
    
    jd = ShopvonsCrawler()
    jd.getall()
 

