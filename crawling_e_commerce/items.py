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

class EcommerceItem(scrapy.Item):
    site_name = scrapy.Field()
    product_name = scrapy.Field()
    product_price = scrapy.Field()
    product_url = scrapy.Field()
    product_image_url = scrapy.Field()
    product_image = scrapy.Field()
    image_urls = scrapy.Field()

    def clean_price(self, price, separator):
        argument = split_string(self, text=price, separator=separator)
        new_price = split_string(self, text=argument[1], separator=".")
        
        return int(''.join(new_price))

    def download_images(self, url, filename):
        response = requests.get(url, stream=True)
        EcommerceItem.save_image_to_file(self, response, filename)
        time.sleep(1)
        del response

    def save_image_to_file(self, image, filename):
        with open('{dirname}/{filename}.jpg'.format(dirname='images', filename=filename), 'wb') as out_file:
            shutil.copyfileobj(image.raw, out_file)

    def clean_image_url(self, url, separator):
        result_image_url = split_string(self, url, separator)
        return result_image_url

    def get_image_filename(self, url, separator):
        result_image_filename = split_string(self, url, separator)
        return result_image_filename