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

    def get_category_top(self):
        return "top"

    def get_category_long(self):
        return "long"
    
    def get_category_bottom(self):
        return "bottom"

    def get_category_berrybenka(self, categories):
        category = {
            'culottes': EcommerceItem.get_category_bottom(self),
            'long-pants': EcommerceItem.get_category_bottom(self),
            'short-pants': EcommerceItem.get_category_bottom(self),
            'jeans': EcommerceItem.get_category_bottom(self),
            'leggings': EcommerceItem.get_category_bottom(self),
            'skirts': EcommerceItem.get_category_bottom(self),
            'maxi-dresses': EcommerceItem.get_category_long(self),
            'midi-dresses': EcommerceItem.get_category_long(self),
            'mini-dresses': EcommerceItem.get_category_long(self),
            'jumpsuit': EcommerceItem.get_category_long(self),
            'casual': EcommerceItem.get_category_long(self),
            'bodycon-dress': EcommerceItem.get_category_long(self),
            'vest': EcommerceItem.get_category_top(self),
            'cardigans': EcommerceItem.get_category_top(self),
            'tank-top': EcommerceItem.get_category_top(self),
            'women-tees': EcommerceItem.get_category_top(self),
            'women-shirts': EcommerceItem.get_category_top(self),
            'blouse': EcommerceItem.get_category_top(self)
        }
        
        return category.get(categories,"category")