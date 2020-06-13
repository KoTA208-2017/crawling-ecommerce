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
from ..items import EcommerceItem

class ZaloraSpider(scrapy.Spider):
    name = 'zalora'
    allowed_domains = ['www.zalora.co.id']
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1200x600')

    def __init__(self):
        self.start_urls = ['https://www.zalora.co.id/women/pakaian/?page=2&category_id=18']
        self.driver = webdriver.Chrome(chrome_options=ZaloraSpider.options)

    def parse(self, response):
        """Function to process clothes category results page"""
        site_name = "Zalora"
        self.driver.get(response.url)
        products=self.driver.find_elements_by_xpath('//*[(@class="b-catalogList__itm hasOverlay unit size1of3")]')

        # item containers for storing product
        items = EcommerceItem()

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
            product_price = EcommerceItem.clean_price(self, product_price, "Rp ")
            product_image_link = ''.join(raw_product_image_link).strip(
            ) if raw_product_image_link else None
            product_link = ''.join(raw_product_link).strip(
            ) if raw_product_link else None

            # select category
            product_category = EcommerceItem.get_category(self, response.request.url, site_name)

            # download image
            image_filename = EcommerceItem.get_image_filename(self, raw_product_image_link, ".com/")
            image_filename = EcommerceItem.get_image_filename(self, image_filename[1], "=/")
            image_filename = "z_" + image_filename[0]
            raw_product_image_link = EcommerceItem.clean_image_link(self, raw_product_image_link, "fff)/")
            raw_product_image_link = raw_product_image_link[1]
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