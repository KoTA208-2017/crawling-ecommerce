# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import requests
import shutil
import time

def split_string(self, text, separator):
    txt = str(text)
    result_url = txt.split(separator)
    return result_url

def category_top(self):
    return "top"

def category_long(self):
    return "long"

def category_bottom(self):
    return "bottom"

class EcommerceItem(scrapy.Item):
    site_name = scrapy.Field()
    product_name = scrapy.Field()
    product_price = scrapy.Field()
    product_url = scrapy.Field()
    product_category = scrapy.Field()
    product_image_url = scrapy.Field()
    product_image = scrapy.Field()
    image_urls = scrapy.Field()

    def get_category(self, url, site_name):
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
            'culottes': category_bottom(self),
            'long-pants': category_bottom(self),
            'short-pants': category_bottom(self),
            'jeans': category_bottom(self),
            'leggings': category_bottom(self),
            'skirts': category_bottom(self),
            'maxi-dresses': category_long(self),
            'midi-dresses': category_long(self),
            'mini-dresses': category_long(self),
            'jumpsuit': category_long(self),
            'casual': category_long(self),
            'bodycon-dress': category_long(self),
            'vest': category_top(self),
            'cardigans': category_top(self),
            'tank-top': category_top(self),
            'women-tees': category_top(self),
            'women-shirts': category_top(self),
            'blouse': category_top(self)
        }
        
        return categories.get(str(category),"category")

    def get_category_jeans_mapemall(self, category):
        categories = {
            '113': category_top(self),
            '119': category_top(self),
            '121': category_top(self),
            '118': category_bottom(self)
        }
        
        return categories.get(category, "category")

    def get_category_mapemall(self, url):
        argument = split_string(self, text=url, separator="ct=")
        categories = split_string(self, text=argument[1], separator="-")
        
        category = {
            '8': category_top(self),
            '9': category_top(self),
            '10': category_bottom(self),
            '11': category_long(self),
            '13': EcommerceItem.get_category_jeans_mapemall(self, category=categories[3])
        }
        
        return category.get(categories[2], "category")

    def get_category_zalora(self, url):
        argument = split_string(self, text=url, separator="id=")

        categories = {
            '175': category_top(self),
            '704': category_top(self),
            '16': category_bottom(self),
            '18': category_bottom(self),
            '17': category_bottom(self),
            '2878': category_bottom(self),
            '25': category_long(self)
        }
        
        return categories.get(str(argument[1]), "category")

    def clean_price(self, price, separator):
        argument = split_string(self, text=price, separator=separator)
        new_price = split_string(self, text=argument[1], separator=".")
        
        return int(''.join(new_price))

    def download_images(self, link, filename):
        response = requests.get(link, stream=True)
        EcommerceItem.save_image_to_file(self, response, filename)
        time.sleep(1)
        del response

    def save_image_to_file(self, image, filename):
        with open('{dirname}/{filename}.jpg'.format(dirname='images', filename=filename), 'wb') as out_file:
            shutil.copyfileobj(image.raw, out_file)

    def clean_image_link(self, url, separator):
        result_image_url = split_string(self, url, separator)
        return result_image_url

    def get_image_filename(self, url, separator):
        result_image_filename = split_string(self, url, separator)
        return result_image_filename