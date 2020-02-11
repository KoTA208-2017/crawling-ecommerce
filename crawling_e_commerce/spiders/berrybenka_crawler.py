# -*- coding: utf-8 -*-
import scrapy
import csv
import os
import logging

from ..items import CrawlingECommerceItem

class BerrybenkaCrawlerSpider(scrapy.Spider):
    name = 'berrybenka_crawler'
    separator = 'n/'
    allowed_domains = ['berrybenka.com']
    start_urls = ['https://berrybenka.com']

    def start_requests(self):
        """Read category_text from categories file amd construct the URL"""

        with open(os.path.join(os.path.dirname(__file__), "../resources/berrybenka_categories.csv")) as categories:
            for category in csv.DictReader(categories):
                category_text=category["category"]
                url=str(BerrybenkaCrawlerSpider.start_urls[0])+"/clothing/"+category_text+"/women/0"
                # The meta is used to send our search text into the parser as metadata
                yield scrapy.Request(url, callback = self.parse, meta = {"category_text": category_text})

    def parse(self, response):
        """Function to process clothes category results page"""
        product_category=response.meta["category_text"]
        products=response.xpath("//*[(@id='li-catalog')]")
        
        # item containers for storing product
        items = CrawlingECommerceItem()
        
        # iterating over search results
        for product in products:
            # Defining the XPaths
            XPATH_PRODUCT_LINK=".//a/@href"
            XPATH_PRODUCT_NAME=".//div[@class='catalog-detail']//div[@class='detail-left']//h1/text()"
            XPATH_PRODUCT_PRICE=".//div[@class='catalog-detail']//div[@class='detail-right']//p/text()"
            XPATH_PRODUCT_IMAGE_LINK=".//div[@class='catalog-image']//img/@src"

            raw_product_name=product.xpath(XPATH_PRODUCT_NAME).get()
            raw_product_price=product.xpath(XPATH_PRODUCT_PRICE).get()
            raw_product_image_link=product.xpath(XPATH_PRODUCT_IMAGE_LINK).extract()
            raw_product_link=product.xpath(XPATH_PRODUCT_LINK).get()
            
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
                product_name=product_name,
                product_price=product_price,
                product_url=product_link,
                product_category=product_category,
                image_urls=raw_product_image_link
            )

            # yield items
        
        XPATH_PRAGINATION_LINK="//*[(@class='next right')]/a/@href"

        next_page = response.xpath(XPATH_PRAGINATION_LINK).get()
        current_url = str(response.request.url)
        current_url = current_url.split(BerrybenkaCrawlerSpider.separator,1)
        number_product = int(current_url[1])
        
        if next_page is not None:
            number_product += 48
            next_url = current_url[0] + BerrybenkaCrawlerSpider.separator + str(number_product)
            logging.info("current URL %s", next_url)
            yield response.follow(next_url, callback = self.parse, meta = {"category_text": product_category})