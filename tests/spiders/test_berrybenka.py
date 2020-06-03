import unittest2 as unittest
from selenium import webdriver
from selenium.webdriver import Chrome

class BerrybenkaTest(unittest.TestCase):
    def setUp(self):
        # create a new Firefox session
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        # navigate to the application home page
        self.driver.get("https://berrybenka.com/clothing/culottes/women/0")

    def test_starts_request(self):
        pass

    def tearDown(self):
        # close the browser window
        self.driver.quit()
        
if __name__ == '__main__':
    unittest.main()