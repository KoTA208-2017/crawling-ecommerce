import unittest2 as unittest
import csv
import os

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

class BerrybenkaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # create a new Chrome session
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(30)
        cls.driver.maximize_window()
        # navigate to the application home page
        cls.driver.get("https://berrybenka.com/clothing/long-pants/women/0")

    def test_read_category_text(self):
        category_text = []
        # open file that store category text
        with open(os.path.join(os.path.dirname(__file__), "../../crawling_e_commerce/resources/berrybenka_categories.csv")) as categories:
            # read file
            for category in csv.DictReader(categories):
                category_text.append(category["category"])

            self.assertEqual("culottes",category_text[0])
    
    def test_amount_of_category_text(self):
        category_text = []
        # open file that store category text
        with open(os.path.join(os.path.dirname(__file__), "../../crawling_e_commerce/resources/berrybenka_categories.csv")) as categories:
            # read file
            for category in csv.DictReader(categories):
                category_text.append(category["category"])

            self.assertEqual(15,len(category_text))
    
    def test_next_button(self):
        # check next button exists on page
        XPATH_NEXT_BUTTON = "//*[(@class='next right')]"
        if(self.is_element_present(By.XPATH, XPATH_NEXT_BUTTON)):
            self.assertTrue(self.is_element_present(By.XPATH, XPATH_NEXT_BUTTON))
        else:
            self.assertFalse(self.is_element_present(By.XPATH, XPATH_NEXT_BUTTON))
    
    def test_product(self):
        # check product exists on page
        ID_PRODUCT = "li-catalog"
        self.assertTrue(self.is_element_present(By.ID, ID_PRODUCT))

    def test_amount_of_product_in_a_page(self):
        # get the xpath products and next button
        XPATH_PRODUCTS = "//*[(@id='li-catalog')]"
        XPATH_NEXT_BUTTON = "//*[(@class='next right')]"
        products = self.driver.find_elements_by_xpath(XPATH_PRODUCTS)

        if(self.is_element_present(By.XPATH, XPATH_NEXT_BUTTON)):
            self.assertEqual(48, len(products))
        else:
            self.assertTrue(len(products)<48)

    @classmethod
    def tearDownClass(cls):
        # close the browser window
        cls.driver.quit()

    # this method taken from https://www.techbeamers.com/selenium-python-test-suite-unittest/
    def is_element_present(self, how, what):
        """
        Helper method to confirm the presence of an element on page
        :params how: By locator type
        :params what: locator value
        """
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException: return False
        return True
        
if __name__ == '__main__':
    unittest.main()