# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector

class CrawlingECommercePipeline(object):

    def __init__(self):
        self.create_connection()
        self.crete_table()
    
    def create_connection(self):
        self.conn=mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='goler88byb',
            database='product'
        )
        self.curr=self.conn.cursor()

    def crete_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS tbm_products_ecommerce""")
        self.curr.execute("""CREATE TABLE tbm_products_ecommerce(
                            product_name text,
                            product_price text,
                            product_category text,
                            product_url text,
                            image text,
                            image_url text
                        )""")

    def process_item(self, item, spider):
        self.store_db(item)   
        return item

    def store_db(self,item):
        self.curr.execute("""INSERT INTO tbm_products_ecommerce values (%s,%s,%s,%s,%s,%s)""", (
            item['product_name'],
            item['product_price'],
            item['product_category'],
            item['product_url'],
            item['image_urls'][0]
        ))
        self.conn.commit()
