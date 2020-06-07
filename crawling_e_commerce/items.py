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

    def select_category_top(self):
        return "top"

    def select_category_long(self):
        return "long"
    
    def select_category_bottom(self):
        return "bottom"

    def select_category_berrybenka(self, categories):
        category = {
            'culottes': EcommerceItem.select_category_bottom(self),
            'long-pants': EcommerceItem.select_category_bottom(self),
            'short-pants': EcommerceItem.select_category_bottom(self),
            'jeans': EcommerceItem.select_category_bottom(self),
            'leggings': EcommerceItem.select_category_bottom(self),
            'skirts': EcommerceItem.select_category_bottom(self),
            'maxi-dresses': EcommerceItem.select_category_long(self),
            'midi-dresses': EcommerceItem.select_category_long(self),
            'mini-dresses': EcommerceItem.select_category_long(self),
            'jumpsuit': EcommerceItem.select_category_long(self),
            'casual': EcommerceItem.select_category_long(self),
            'bodycon-dress': EcommerceItem.select_category_long(self),
            'vest': EcommerceItem.select_category_top(self),
            'cardigans': EcommerceItem.select_category_top(self),
            'tank-top': EcommerceItem.select_category_top(self),
            'women-tees': EcommerceItem.select_category_top(self),
            'women-shirts': EcommerceItem.select_category_top(self),
            'blouse': EcommerceItem.select_category_top(self)
        }
        
        return category.get(categories,"category")