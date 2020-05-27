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
from selenium.common.exceptions import NoSuchElementException
from ..items import CrawlingECommerceItem
from ..split_string import SplitString
from ..category import Category

class ZaloraCrawlerSpider(scrapy.Spider):
    name = 'zalora_crawler'
    allowed_domains = ['www.zalora.co.id']
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1200x600')

    def __init__(self):
        self.start_urls = ['https://www.zalora.co.id/women/pakaian/?page=2&category_id=18']
        self.driver = webdriver.Chrome(chrome_options=ZaloraCrawlerSpider.options)

    def parse(self, response):
        """Function to process clothes category results page"""
        self.driver.get(response.url)
        products=self.driver.find_elements_by_xpath('//*[(@class="b-catalogList__itm hasOverlay unit size1of3")]')

        # item containers for storing product
        items = CrawlingECommerceItem()

        # wait to scoll page
        time.sleep(30)

        # iterating over search results
        for product in products:
            # Defining the XPaths
            XPATH_PRODUCT_LINK = './/a[@class="b-catalogList__itmLink itm-link"]'
            XPATH_PRODUCT_NAME = './/em'
            XPATH_PRODUCT_SPECIAL_PRICE = './/span[@class="b-catalogList__itmPrice special"]'
            XPATH_PRODUCT_PRICE = './/span[@class="b-catalogList__itmPrice"]'
            XPATH_PRODUCT_IMAGE_LINK = './/img[@class="b-catalogList__itm-img b-catalogList__itm-img"]'

            try:
                raw_product_price = product.find_element_by_xpath(XPATH_PRODUCT_SPECIAL_PRICE).text
            except NoSuchElementException:
                raw_product_price = product.find_element_by_xpath(XPATH_PRODUCT_PRICE).text

            raw_product_name = product.find_element_by_xpath(XPATH_PRODUCT_NAME).text
            raw_product_image_link = product.find_element_by_xpath(XPATH_PRODUCT_IMAGE_LINK).get_attribute("src")
            raw_product_link = product.find_element_by_xpath(XPATH_PRODUCT_LINK).get_attribute("href")
            
            logging.info("image link %s", raw_product_image_link)

            # cleaning the data
            product_name = ''.join(raw_product_name).strip(
            ) if raw_product_name else None
            product_price = ''.join(raw_product_price).strip(
            ) if raw_product_price else None
            product_image_link = ''.join(raw_product_image_link).strip(
            ) if raw_product_image_link else None
            product_link = ''.join(raw_product_link).strip(
            ) if raw_product_link else None
            product_price = ZaloraCrawlerSpider.clean_product_price(self,product_price)

            # select category
            product_category = ZaloraCrawlerSpider.select_category(self, response.request.url)

            # create image directory
            dirname = 'images'
            ZaloraCrawlerSpider.make_dir(self, dirname)

            # download image
            image_filename = ZaloraCrawlerSpider.split_image_filename(self, raw_product_image_link)
            raw_product_image_link = ZaloraCrawlerSpider.split_image_url(self, raw_product_image_link)
            ZaloraCrawlerSpider.download_images(self, dirname, raw_product_image_link, image_filename)

            # storing item
            yield CrawlingECommerceItem (
                site_name = 'Zalora',
                product_name = product_name,
                product_price = product_price,
                product_url = product_link,
                product_category = product_category,
                product_image_url = raw_product_image_link,
                product_image = image_filename + '.jpg'
            )

        self.driver.close()

    def clean_product_price(self,product_price):
        price = SplitString.action(self,product_price,"Rp ")
        price = SplitString.action(self,price[1],".")
        return int(''.join(price))

    def make_dir(self,dirname):
        current_path = os.getcwd()
        path = os.path.join(current_path, dirname)
        if not os.path.exists(path):
            os.makedirs(path)

    def download_images(self,dirname, link, raw_product_name):
        response = requests.get(link, stream=True)
        ZaloraCrawlerSpider.save_image_to_file(self, response, dirname, raw_product_name)
        time.sleep(3)
        del response

    def save_image_to_file(self,image, dirname, suffix):
        with open('{dirname}/{suffix}.jpg'.format(dirname=dirname, suffix=suffix), 'wb') as out_file:
            shutil.copyfileobj(image.raw, out_file)

    def split_image_url(self, url):
        separator = 'fff)/'
        result_image_url = SplitString.action(self, url, separator)
        return result_image_url[1]

    def split_image_filename(self, url):
        separator = '.com/'
        result_image_filename = SplitString.action(self, url, separator)
        separator = '=/'
        result_image_filename = SplitString.action(self, result_image_filename[1], separator)
        return 'z_' + result_image_filename[0]

    def split_url(self, url):
        separator = 'id='
        result_url = SplitString.action(self, url, separator)
        return result_url[1]

    def select_category(self, url):
        argument = ZaloraCrawlerSpider.split_url(self, url)
        logging.info("argument %s", argument)
        
        category = {
            '175': Category.select_top(self),
            '704': Category.select_top(self),
            '16': Category.select_bottom(self),
            '18': Category.select_bottom(self),
            '17': Category.select_bottom(self),
            '2878': Category.select_bottom(self),
            '25': Category.select_long(self)
        }
        
        return category.get(str(argument), "category")