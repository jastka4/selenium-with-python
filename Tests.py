import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

class KytaryOrgSearch(unittest.TestCase):

    def setUp(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        self.driver = webdriver.Firefox(executable_path=current_path + '/geckodriver')

    def test_add_to_cart(self):
        driver = self.driver
        driver.get("https://kytary.pl/")
        self.assertIn("Instrumenty muzyczne", driver.title)

        search = driver.find_element_by_id("search")

        search.send_keys("pocket operator")
        search.send_keys(Keys.RETURN)
    
        try:
            search_page_loaded = WebDriverWait( driver, 10 ).until(EC.title_contains("Wyszukiwanie")
        )
        except TimeoutException:
            self.fail( "Loading search page timeout expired" )

        item = driver.find_element_by_class_name("product-list__item").click()
        
        try:
            add_to_cart_button = WebDriverWait( driver, 5 ).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.submit-div.to-cart-button')))
        except TimeoutException:
            self.fail( "Loading product page timeout expired" )
        except NoSuchElementException:
            self.fail( "Couldn't find add to cart button" )

        try:
            add_to_cart_button.click()
            WebDriverWait( driver, 5).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.submit-div.to-cart-button'), '1 szt w koszyku'))
        except TimeoutException:
            self.fail( "Loading product page timeout expired" )
        except NoSuchElementException:
            self.fail( "Couldn't add to cart" )

        assert "No results found." not in driver.page_source


    def tearDown(self):
        driver = self.driver
        mini_cart = driver.find_elements_by_css_selector('.list-container')[0]
        item_in_cart = mini_cart.find_element_by_xpath('.//div[1]/ul/li/span[5]/a/i')
        item_in_cart.click()
        driver.close()

if __name__ == "__main__":
    unittest.main()