# -*- coding: utf-8 -*-
import scrapy
import csv
import os
import logging
import time
import requests
import shutil

from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from ..items import EcommerceItem

class BerrybenkaSpider(scrapy.Spider):
    name = 'berrybenka'
    separator = 'n/'
    allowed_domains = ['berrybenka.com']
    start_urls = ['https://berrybenka.com']

    def start_requests(self):
        """Read category_text from categories file amd construct the URL"""

        with open(os.path.join(os.path.dirname(__file__), "../resources/berrybenka_categories.csv")) as categories:
            for category in csv.DictReader(categories):
                category_text = category["category"]
                url = str(BerrybenkaSpider.start_urls[0])+"/clothing/"+category_text+"/women/0"
                # The meta is used to send our search text into the parser as metadata
                yield scrapy.Request(url, callback = self.parse, meta = {"category_text": category_text})

    def parse(self, response):
        """Function to process clothes category results page"""
        site_name = "Berrybenka"
        product_category = response.meta["category_text"]
        products = response.xpath("//*[(@id='li-catalog')]")
        
        # item containers for storing product
        items = EcommerceItem()
        
        # iterating over search results
        for product in products:
            # Defining the XPaths
            XPATH_PRODUCT_LINK = ".//a/@href"
            XPATH_PRODUCT_NAME = ".//div[@class='catalog-detail']//div[@class='detail-left']//h1/text()"
            XPATH_PRODUCT_PRICE = ".//div[@class='catalog-detail']//div[@class='detail-right']//p/text()"
            XPATH_PRODUCT_IMAGE_LINK = ".//div[@class='catalog-image']//img/@src"

            raw_product_name = product.xpath(XPATH_PRODUCT_NAME).get()
            raw_product_price = product.xpath(XPATH_PRODUCT_PRICE).get()
            raw_product_image_link = product.xpath(XPATH_PRODUCT_IMAGE_LINK).extract()
            raw_product_link = product.xpath(XPATH_PRODUCT_LINK).get()
            
            # cleaning the data
            product_name = ''.join(raw_product_name).strip(
            ) if raw_product_name else None
            product_price = ''.join(raw_product_price).strip(
            ) if raw_product_price else None
            product_price = EcommerceItem.clean_price(self, product_price, "IDR")
            product_image_link = ''.join(raw_product_image_link).strip(
            ) if raw_product_image_link else None
            product_link = ''.join(raw_product_link).strip(
            ) if raw_product_link else None

            # split image link
            product_image_link = str(raw_product_image_link[0])
            template = "https://im.berrybenka.com/assets/cache/300x456/product-overlay/_VDEGZ_2836.png"
            if(product_image_link == template):
                image_link = EcommerceItem.clean_image_url(self, str(raw_product_image_link[1]), "cache/300x456")
                raw_product_image_link[0] = image_link[0] + "upload" + image_link[1]
            else:
                image_link = EcommerceItem.clean_image_url(self, str(raw_product_image_link[0]), "cache/300x456")
                raw_product_image_link[0] = image_link[0] + "upload" + image_link[1]

            # storing item
            yield EcommerceItem (
                site_name = site_name,
                product_name = product_name,
                product_price = product_price,
                product_url = product_link,
                image_urls = raw_product_image_link
            )
        
        XPATH_PRAGINATION_LINK="//*[(@class='next right')]/a/@href"

        next_page = response.xpath(XPATH_PRAGINATION_LINK).get()
        current_url = str(response.request.url)
        current_url = current_url.split(BerrybenkaSpider.separator,1)
        number_product = int(current_url[1])
        
        if next_page is not None:
            number_product += 48
            next_url = current_url[0] + BerrybenkaSpider.separator + str(number_product)
            logging.info("current URL %s", next_url)
            yield response.follow(next_url, callback = self.parse, meta = {"category_text": product_category})

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

            # download image
            image_filename = EcommerceItem.get_image_filename(self, raw_product_image_link, ".com/")
            image_filename = EcommerceItem.get_image_filename(self, image_filename[1], "=/")
            image_filename = "z_" + image_filename[0]
            raw_product_image_link = EcommerceItem.clean_image_url(self, raw_product_image_link, "fff)/")
            raw_product_image_link = raw_product_image_link[1]
            EcommerceItem.download_images(self, raw_product_image_link, image_filename)

            # storing item
            yield EcommerceItem (
                site_name = site_name,
                product_name = product_name,
                product_price = product_price,
                product_url = product_link,
                product_image_url = raw_product_image_link,
                product_image = image_filename + '.jpg'
            )

        self.driver.close()

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

            # download image
            raw_product_image_link = EcommerceItem.clean_image_url(self, raw_product_image_link, "?x-oss")
            raw_product_image_link = raw_product_image_link[0]
            image_filename = EcommerceItem.get_image_filename(self, raw_product_image_link, "/")
            image_filename = 'm_' + image_filename[4]
            EcommerceItem.download_images(self, raw_product_image_link, image_filename)

            # storing item
            yield EcommerceItem (
                site_name = site_name,
                product_name = product_name,
                product_price = product_price,
                product_url = product_link,
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

process = CrawlerProcess()
process.crawl(MapemallSpider)
process.crawl(ZaloraSpider)
process.crawl(BerrybenkaSpider)
process.start() 