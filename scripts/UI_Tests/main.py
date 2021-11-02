# coding=utf8
import os
import random
import string

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from selenium.common.exceptions import NoSuchElementException 

driver = webdriver.Chrome(r'C:\Users\julek\Desktop\Lampy_PrestaShop\scripts\ImportSeleniumScript\seleniumdriver\win\chromedriver.exe')
driver.maximize_window()

def add_items_to_cart(category_url, count):

    page = 1
    for i in range(0,count):

        if page == 1:
            driver.get(category_url)
        else:
            driver.get(category_url+"?page="+page)
        
        product = driver.find_elements_by_css_selector(".product-title > a")[i%12]
        driver.get(product.get_attribute("href"))
        try:
   
            quantity = driver.find_elements_by_css_selector(".product-quantities > span")[0].get_attribute("data-stock")

            no_of_products = random.randint(1,int(quantity))-1

            up_button = driver.find_elements_by_css_selector(".btn.btn-touchspin.js-touchspin.bootstrap-touchspin-up")[0]
            
            for _ in range(0,random.randint(0,no_of_products)):
                up_button.click()

            driver.find_elements_by_css_selector(".add-to-cart")[0].click()

        except NoSuchElementException:
            count+=1
            if count%12==0:
                page+=1



def delete_one_item():
    driver.get("https://localhost/koszyk")

    elements_count = len(driver.find_elements_by_css_selector("i.material-icons.float-xs-left"))

    driver.find_elements_by_css_selector("i.material-icons.float-xs-left")[random.randint(0,elements_count)].click()

def create_account():
    driver.get("https://localhost/zam%C3%B3wienie")
    driver.find_elements_by_css_selector(".radio-inline")[random.randint(0,2)].click()

    letters = string.ascii_letters

    name = driver.find_element_by_xpath('//input[@name="firstname"]')
    name.clear()
    name.send_keys((''.join(random.choice(letters) for i in range(random.randint(8,15)))))

    lastname = driver.find_element_by_xpath('//input[@name="lastname"]')
    lastname.clear()
    lastname.send_keys((''.join(random.choice(letters) for i in range(random.randint(8,15)))))
    # dokonczyc tutaj


lamps_count = 10

count_from_first_tab = random.randint(1,lamps_count-1)
count_from_second_tab = lamps_count - count_from_first_tab

add_items_to_cart("https://localhost/3-nowoczesne",count_from_first_tab)
add_items_to_cart("https://localhost/14-lazienkowe",count_from_second_tab)
delete_one_item()
create_account()
