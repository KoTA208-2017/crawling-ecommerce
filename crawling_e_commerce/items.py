# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class EcommerceItem(scrapy.Item):
    site_name = scrapy.Field()
    product_name = scrapy.Field()
    product_price = scrapy.Field()
    product_url = scrapy.Field()
    product_category = scrapy.Field()
    product_image_url = scrapy.Field()
    product_image = scrapy.Field()
