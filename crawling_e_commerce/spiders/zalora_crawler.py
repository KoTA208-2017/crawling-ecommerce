# -*- coding: utf-8 -*-
import scrapy


class ZaloraCrawlerSpider(scrapy.Spider):
    name = 'zalora_crawler'
    allowed_domains = ['www.zalora.co.id']
    start_urls = ['http://www.zalora.co.id/']

    def parse(self, response):
        pass
