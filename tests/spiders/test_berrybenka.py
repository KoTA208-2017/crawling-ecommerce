import unittest2 as unittest
import csv
import os

from selenium import webdriver
from selenium.webdriver import Chrome

class BerrybenkaTest(unittest.TestCase):
    def setUp(self):
        # create a new Chrome session
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        # navigate to the application home page
        self.driver.get("https://berrybenka.com/clothing/culottes/women/0")

    def test_read_category_text(self):
        category_text = []
        # open file that store category text
        with open(os.path.join(os.path.dirname(__file__), "../../crawling_e_commerce/resources/berrybenka_categories.csv")) as categories:
            # read file
            for category in csv.DictReader(categories):
                category_text.append(category["category"])

            self.assertEqual("culottes",category_text[0])
    
    def test_count_category_text(self):
        category_text = []
        with open(os.path.join(os.path.dirname(__file__), "../../crawling_e_commerce/resources/berrybenka_categories.csv")) as categories:
            for category in csv.DictReader(categories):
                category_text.append(category["category"])

            self.assertEqual(15,len(category_text))

    def tearDown(self):
        # close the browser window
        self.driver.quit()
        
if __name__ == '__main__':
    unittest.main()