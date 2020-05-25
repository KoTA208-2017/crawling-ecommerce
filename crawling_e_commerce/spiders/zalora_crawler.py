# -*- coding: utf-8 -*-
import scrapy
import csv
import os
import logging

from ..items import CrawlingECommerceItem

class ZaloraCrawlerSpider(scrapy.Spider):
    name = 'zalora_crawler'
    allowed_domains = ['www.zalora.co.id']
    start_urls = ['http://www.zalora.co.id/']

    def start_requests(self):
        """Read category_text from categories file and construct the URL"""

        with open(os.path.join(os.path.dirname(__file__), "../resources/zalora_categories.csv")) as categories:
            for category in csv.DictReader(categories):
                category_text=category["category"]
                url=str(ZaloraCrawlerSpider.start_urls[0])+"/women/pakaian/?page=1&category_id="+category_text
                # The meta is used to send our search text into the parser as metadata
                yield scrapy.Request(url, callback = self.parse, meta = {"category_text": category_text})

    def parse(self, response):
        """Function to process clothes category results page"""
        product_category=response.meta["category_text"]
        products=response.xpath('//*[(@class="b-catalogList__itm hasOverlay unit size1of3")]')

        # item containers for storing product
        items = CrawlingECommerceItem()