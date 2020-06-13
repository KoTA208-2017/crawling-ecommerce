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
from ..items import EcommerceItem
from ..split_string import SplitString
from ..category import Category

class MapemallSpider(scrapy.Spider):
    name = 'mapemall'
    allowed_domains = ['www.mapemall.com']
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1200x600')

    def __init__(self):
        self.start_urls = ['https://www.mapemall.com/forher/clothing?ct=1-7-13-113']
        self.driver = webdriver.Chrome(chrome_options=MapemallSpider.options)

    def parse(self, response):
        """Function to process clothes results page"""
        site_name = "Mapemall"
        self.driver.get(response.url)

        # scroll page
        MapemallSpider.scroll(self, 5)

        # item containers for storing product
        items = EcommerceItem()

        # iterating over search results
        products = self.driver.find_elements_by_xpath('//*[(@class="col-12-3 col-sm-12-6 list-item")]')
        for product in products:
            # Defining the XPaths
            XPATH_PRODUCT_NAME = './/div[@class="goods-tit"]//a'
            XPATH_PRODUCT_PRICE = './/div[@class="goods-price special-price"]//span'
            XPATH_PRODUCT_IMAGE_LINK = './/div[@class="img-box"]/a/img'
            XPATH_PRODUCT_LINK = './/div[@class="goods-tit"]//a'

            raw_product_name = product.find_element_by_xpath(XPATH_PRODUCT_NAME).text
            raw_product_price = product.find_element_by_xpath(XPATH_PRODUCT_PRICE).text
            raw_product_image_link = product.find_element_by_xpath(XPATH_PRODUCT_IMAGE_LINK).get_attribute("src")
            raw_product_link = product.find_element_by_xpath(XPATH_PRODUCT_LINK).get_attribute("href")

            # cleaning the data
            product_name = ''.join(raw_product_name).strip(
            ) if raw_product_name else None
            product_price = ''.join(raw_product_price).strip(
            ) if raw_product_price else None
            product_price = EcommerceItem.clean_price(self, product_price, ". ")
            product_image_link = ''.join(raw_product_image_link).strip(
            ) if raw_product_image_link else None
            product_link = ''.join(raw_product_link).strip(
            ) if raw_product_link else None
            
            # select category
            product_category = EcommerceItem.get_category(self, response.request.url, site_name)

            # download image
            raw_product_image_link = EcommerceItem.clean_image_link(self, raw_product_image_link, "?x-oss")
            raw_product_image_link = raw_product_image_link[0]
            image_filename = MapemallSpider.split_image_filename(self, raw_product_image_link)
            EcommerceItem.download_images(self, raw_product_image_link, image_filename)

            # storing item
            yield EcommerceItem (
                site_name = site_name,
                product_name = product_name,
                product_price = product_price,
                product_url = product_link,
                product_category = product_category,
                product_image_url = raw_product_image_link,
                product_image = image_filename + '.jpg'
            )

        self.driver.close()

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
    
    def split_image_filename(self, url):
        separator = '/'
        result_image_filename = SplitString.action(self, url, separator)
        return 'm_' + result_image_filename[4]