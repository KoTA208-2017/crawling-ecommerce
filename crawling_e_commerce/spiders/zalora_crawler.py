# -*- coding: utf-8 -*-
import scrapy
import csv
import os
import logging

from ..items import CrawlingECommerceItem
from selenium import webdriver
from selenium.webdriver import Chrome

class ZaloraCrawlerSpider(scrapy.Spider):
    name = 'zalora_crawler'
    allowed_domains = ['www.zalora.co.id']
    start_urls = ['http://www.zalora.co.id']
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1200x600')

    def __init__(self):
        self.start_urls = ['https://www.zalora.co.id/women/pakaian/?category_id=18']
        self.driver = webdriver.Chrome(chrome_options=ZaloraCrawlerSpider.options)

    def parse(self, response):
        """Function to process clothes category results page"""
        self.driver.get(response.url)
        products=self.driver.find_elements_by_xpath('//*[(@class="b-catalogList__itm hasOverlay unit size1of3")]')

        # item containers for storing product
        items = CrawlingECommerceItem()

        # iterating over search results
        for product in products:
            # Defining the XPaths
            XPATH_PRODUCT_LINK='.//a[@class="b-catalogList__itmLink itm-link"]'
            XPATH_PRODUCT_NAME='.//em'
            XPATH_PRODUCT_PRICE='.//span[@class="b-catalogList__itmPrice special"]'
            XPATH_PRODUCT_IMAGE_LINK='.//img[@class="b-catalogList__itm-img b-catalogList__itm-img"]'

            raw_product_name = product.find_element_by_xpath(XPATH_PRODUCT_NAME).text
            raw_product_price = product.find_element_by_xpath(XPATH_PRODUCT_PRICE).text
            raw_product_image_link = product.find_element_by_xpath(XPATH_PRODUCT_IMAGE_LINK).get_attribute("src")
            raw_product_link = product.find_element_by_xpath(XPATH_PRODUCT_LINK).get_attribute("href")
            
            print("!print" + raw_product_image_link)

            # cleaning the data
            product_name=''.join(raw_product_name).strip(
            ) if raw_product_name else None
            product_price=''.join(raw_product_price).strip(
            ) if raw_product_price else None
            product_image_link=''.join(raw_product_image_link).strip(
            ) if raw_product_image_link else None
            product_link=''.join(raw_product_link).strip(
            ) if raw_product_link else None

            # storing item
            yield CrawlingECommerceItem (
                site_name = 'Zalora',
                product_name = product_name,
                product_price = product_price,
                product_url = product_link,
                product_category = "category",
                product_image_url = raw_product_image_link,
                product_image = '.jpg'
            )