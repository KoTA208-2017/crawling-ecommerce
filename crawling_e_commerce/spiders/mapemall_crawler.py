# -*- coding: utf-8 -*-
import scrapy
import csv
import os
import logging
import time
import requests
import shutil

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.common.exceptions import ElementNotInteractableException
from ..items import CrawlingECommerceItem

class MapemallCrawlerSpider(scrapy.Spider):
    name = 'mapemall_crawler'
    # separator = 'n/'
    allowed_domains = ['www.mapemall.com']
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1200x600')

    def __init__(self):
        self.start_urls = ['https://www.mapemall.com/forher/clothing?ct=1-7-10-102']
        self.driver = webdriver.Chrome(chrome_options=MapemallCrawlerSpider.options)

    def parse(self, response):
        """Function to process clothes results page"""
        self.driver.get(response.url)

        # scroll page
        MapemallCrawlerSpider.scroll(self,5)

        # item containers for storing product
        items = CrawlingECommerceItem()

        # iterating over search results
        products = self.driver.find_elements_by_xpath('//*[(@class="col-12-3 col-sm-12-6 list-item")]')
        for product in products:
            # Defining the XPaths
            XPATH_PRODUCT_NAME='.//div[@class="goods-tit"]//a'
            XPATH_PRODUCT_PRICE='.//div[@class="goods-price special-price"]//span'
            XPATH_PRODUCT_IMAGE_LINK='.//div[@class="img-box"]/a/img'
            XPATH_PRODUCT_LINK='.//div[@class="goods-tit"]//a'

            raw_product_name=product.find_element_by_xpath(XPATH_PRODUCT_NAME).text
            raw_product_price=product.find_element_by_xpath(XPATH_PRODUCT_PRICE).text
            raw_product_image_link=product.find_element_by_xpath(XPATH_PRODUCT_IMAGE_LINK).get_attribute("src")
            raw_product_link=product.find_element_by_xpath(XPATH_PRODUCT_LINK).get_attribute("href")

            # cleaning the data
            product_name=''.join(raw_product_name).strip(
            ) if raw_product_name else None
            product_price=''.join(raw_product_price).strip(
            ) if raw_product_price else None
            product_image_link=''.join(raw_product_image_link).strip(
            ) if raw_product_image_link else None
            product_link=''.join(raw_product_link).strip(
            ) if raw_product_link else None
            product_price=MapemallCrawlerSpider.cleaning_data_product_price(product_price)
            
            # select category
            product_category=MapemallCrawlerSpider.select_category(self,url=response.request.url)

            # create image directory
            dirname='images'
            MapemallCrawlerSpider.make_dir(self,dirname)

            # download image
            raw_product_image_link=MapemallCrawlerSpider.split_image_url(self,url=raw_product_image_link)
            image_filename=MapemallCrawlerSpider.split_image_filename(self,url=raw_product_image_link)
            image_filename='m_'+image_filename
            MapemallCrawlerSpider.download_images(self,dirname, raw_product_image_link, image_filename)

            # storing item
            yield CrawlingECommerceItem (
                site_name='Mapemall',
                product_name=product_name,
                product_price=product_price,
                product_url=product_link,
                product_category=product_category,
                product_image_url=raw_product_image_link,
                product_image=image_filename+'.jpg'
            )

        self.driver.close()

    def cleaning_data_product_price(self,product_price):
        txt=product_price
        price=txt.split(". ")
        price=price[1].split(".")

        price = ''.join(price)
        return int(price)

    def make_dir(self,dirname):
        current_path = os.getcwd()
        path = os.path.join(current_path, dirname)
        if not os.path.exists(path):
            os.makedirs(path)

    def download_images(self,dirname, link, raw_product_name):
        response = requests.get(link, stream=True)
        MapemallCrawlerSpider.save_image_to_file(self,response, dirname, raw_product_name)
        time.sleep(3)
        del response

    def save_image_to_file(self,image, dirname, suffix):
        with open('{dirname}/{suffix}.jpg'.format(dirname=dirname, suffix=suffix), 'wb') as out_file:
            shutil.copyfileobj(image.raw, out_file)
    
    def scroll(self, timeout):
        scroll_pause_time = timeout
        totalPages = int(self.driver.execute_script(" return document.getElementById('totalPages').value"))

        for page in range(1,totalPages):
            view_more = '//*[(@class="load-more")]//div[not(contains(@style,"display:none"))]'
            try:
                self.driver.find_element_by_xpath(view_more).click()
            except ElementNotInteractableException:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(timeout)

    def split_image_url(self, url):
        separator = '?x-oss'
        current_url = str(url)
        category = current_url.split(separator)
        return category[0]
    
    def split_image_filename(self, url):
        separator = '/'

        current_url = str(url)
        category = current_url.split(separator)
        return category[4]

    def split_url(self, url):
        separator = 'ct='

        current_url = str(url)
        category = current_url.split(separator,1)
        return category[1]

    def split_category(self, category):
        separator = '-'

        category = str(category)
        category = category.split(separator,4)
        return category

    def select_category_top(self):
        return "top"

    def select_category_long(self):
        return "long"
    
    def select_category_bottom(self):
        return "bottom"

    def select_category_jeans(self, category):
        cat = {
            '113': MapemallCrawlerSpider.select_category_top(self),
            '119': MapemallCrawlerSpider.select_category_top(self),
            '121': MapemallCrawlerSpider.select_category_top(self),
            '118': MapemallCrawlerSpider.select_category_bottom(self)
        }
        
        return cat.get(category,"category")

    def select_category(self, url):
        argument = MapemallCrawlerSpider.split_url(self,url = url)
        categories = MapemallCrawlerSpider.split_category(self,category=argument)
        
        category = {
            '8': MapemallCrawlerSpider.select_category_top(self),
            '9': MapemallCrawlerSpider.select_category_top(self),
            '10': MapemallCrawlerSpider.select_category_bottom(self),
            '11': MapemallCrawlerSpider.select_category_long(self),
            '13': MapemallCrawlerSpider.select_category_jeans(self,category= categories[3])
        }
        
        return category.get(categories[2],"category")