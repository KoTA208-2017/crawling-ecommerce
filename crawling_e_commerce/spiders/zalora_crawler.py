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