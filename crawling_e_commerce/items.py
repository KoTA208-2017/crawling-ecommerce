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
    image_urls = scrapy.Field()

    def get_category_top(self):
        return "top"

    def get_category_long(self):
        return "long"
    
    def get_category_bottom(self):
        return "bottom"

    def get_category(self, url, site_name):
        print("!sitename " + site_name)
        if(site_name == "Zalora"):
            return EcommerceItem.get_category_zalora(self, url)
        elif(site_name == "Berrybenka"):
            return EcommerceItem.get_category_berrybenka(self, url)
        elif(site_name == "Mapemall"):
            return EcommerceItem.get_category_mapemall(self, url)
        else:
            return None

    def get_category_berrybenka(self, category):
        categories = {
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
        
        return categories.get(str(category),"category")

    def get_category_jeans_mapemall(self, category):
        categories = {
            '113': EcommerceItem.get_category_top(self),
            '119': EcommerceItem.get_category_top(self),
            '121': EcommerceItem.get_category_top(self),
            '118': EcommerceItem.get_category_bottom(self)
        }
        
        return categories.get(category, "category")

    def get_category_mapemall(self, url):
        argument = EcommerceItem.split_string(self, text=url, separator="ct=")
        categories = EcommerceItem.split_string(self, text=argument[1], separator="-")
        
        category = {
            '8': EcommerceItem.get_category_top(self),
            '9': EcommerceItem.get_category_top(self),
            '10': EcommerceItem.get_category_bottom(self),
            '11': EcommerceItem.get_category_long(self),
            '13': EcommerceItem.get_category_jeans_mapemall(self, category=categories[3])
        }
        
        return category.get(categories[2], "category")

    def get_category_zalora(self, url):
        argument = EcommerceItem.split_string(self, text=url, separator="id=")

        categories = {
            '175': EcommerceItem.get_category_top(self),
            '704': EcommerceItem.get_category_top(self),
            '16': EcommerceItem.get_category_bottom(self),
            '18': EcommerceItem.get_category_bottom(self),
            '17': EcommerceItem.get_category_bottom(self),
            '2878': EcommerceItem.get_category_bottom(self),
            '25': EcommerceItem.get_category_long(self)
        }
        
        return categories.get(str(argument[1]), "category")