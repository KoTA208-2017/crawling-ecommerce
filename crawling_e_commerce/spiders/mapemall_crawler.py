# -*- coding: utf-8 -*-
import scrapy
import csv
import os
import logging
import time

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.common.exceptions import ElementNotInteractableException
from ..items import CrawlingECommerceItem

class MapemallCrawlerSpider(scrapy.Spider):
    name = 'mapemall_crawler'
    # separator = 'n/'
    allowed_domains = ['www.mapemall.com']
    start_urls = ['https://www.mapemall.com/forher/clothing?ct=']
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1200x600')

    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options=MapemallCrawlerSpider.options)

    def start_requests(self):
        """Read category_text from categories file amd construct the URL"""

        with open(os.path.join(os.path.dirname(__file__), "../resources/mapemall_categories.csv")) as categories:
            for category in csv.DictReader(categories):
                category_text=category["category"]
                url=str(MapemallCrawlerSpider.start_urls[0])+category_text
                # The meta is used to send our search text into the parser as metadata
                yield scrapy.Request(url, callback = self.parse, meta = {"category_text": category_text})

    def parse(self, response):
        """Function to process clothes category results page"""
        self.driver.get(response.url)
        product_category=response.meta["category_text"]
        # products=response.xpath("//*[(@class='list-item')]")
        
        # item containers for storing product
        items = CrawlingECommerceItem()
        self.driver.get(response.request.url)

        view_more = self.driver.find_element_by_xpath('//*[(@class="load-more")]//div[@class="load-btn"]//a')
        # MapemallCrawlerSpider.scroll(self, self.driver, 5)
        while True:
            view_more = '//*[(@class="load-more")]//div[not(contains(@style,"display:none"))]'

            try:
                self.driver.find_element_by_xpath(view_more).click()
            except ElementNotInteractableException:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
            else: 
                yield response.follow(str(response.request.url), callback = self.parse, meta = {"category_text": product_category})

        # products = self.driver.find_elements_by_xpath('//*[(@class="product-grid")]')
        # source = self.driver.page_source
        # print("!SOURCE "+source)
        
        # iterating over search results
        # for product in products:
        #     # Defining the XPaths
        #     XPATH_PRODUCT_LINK=".//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'goods-tit', ' ' ))]//a"
        #     XPATH_PRODUCT_NAME=".//div[@class='goods-introudce']//a/@href"
        #     XPATH_PRODUCT_PRICE=".//div[@class='catalog-detail']//div[@class='detail-right']//p/text()"
        #     XPATH_PRODUCT_IMAGE_LINK=".//img"

        #     raw_product_name=product.xpath(XPATH_PRODUCT_NAME).get()
        #     raw_product_price=product.xpath(XPATH_PRODUCT_PRICE).get()
        #     raw_product_image_link=product.xpath(XPATH_PRODUCT_IMAGE_LINK).extract()
        #     raw_product_link=product.xpath(XPATH_PRODUCT_LINK).get()

    #         # cleaning the data
    #         product_name=''.join(raw_product_name).strip(
    #         ) if raw_product_name else None
    #         product_price=''.join(raw_product_price).strip(
    #         ) if raw_product_price else None
    #         product_image_link=''.join(raw_product_image_link).strip(
    #         ) if raw_product_image_link else None
    #         product_link=''.join(raw_product_link).strip(
    #         ) if raw_product_link else None

    #         # storing item
    #         yield CrawlingECommerceItem (
    #             product_name=product_name,
    #             product_price=product_price,
    #             product_url=product_link,
    #             product_category=product_category,
    #             image_urls=raw_product_image_link
    #         )

    #         # yield items
        
    #     XPATH_PRAGINATION_LINK="//*[(@class='next right')]/a/@href"

        self.driver.close()
        # yield response.follow(str(response.request.url), callback = self.parse, meta = {"category_text": product_category})

    def scroll(self, driver, timeout):
        scroll_pause_time = timeout

        while True:
            view_more = '//*[(@class="load-more")]//div[not(contains(@style,"display:none"))]'

            try:
                driver.find_element_by_xpath(view_more).click()
            except ElementNotInteractableException:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # time.sleep(scroll_pause_time)
            else: 
                break

    def split_image_url(self, url):
        separator = '?x-oss'

        current_url = str(url)
        category = current_url.split(separator)
        return category[0]

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