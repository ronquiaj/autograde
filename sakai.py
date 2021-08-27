import time
from selenium import webdriver
import os
from dotenv import load_dotenv
import re

load_dotenv()
SAKAI_USERNAME = os.getenv("SAKAI_USERNAME")
SAKAI_PASSWORD = os.getenv("SAKAI_PASSWORD")

desired_class = input("Enter the name of the class you'd like to click on: ")
browser = webdriver.Chrome("C:\\bin\\chromedriver.exe")


"""
Logs in to Sakai through the guest route.
"""
def login(browser):
   
    browser.get("https://sakai.plu.edu/portal")

    guest_login_button = browser.find_element_by_id("loginLink2")
    guest_login_button.click()
    
    time.sleep(1)

    username = browser.find_element_by_id("eid")
    password = browser.find_element_by_id("pw")
    submit_login_button = browser.find_element_by_id("submit")

    username.send_keys(SAKAI_USERNAME)
    password.send_keys(SAKAI_PASSWORD)
    submit_login_button.click()

"""
Iterates through the Sakai tabs on the home page and uses a regex comparison against our query to click on the desired tab
"""
def iterate_through_tabs_and_click(browser, desired_class):
    
    class_regex = re.compile(desired_class, re.IGNORECASE)
    
    tabs = browser.find_elements_by_class_name("Mrphs-sitesNav__menuitem") # The tabs visible in the main menu
    for tab in tabs:
        if (class_regex.search(tab.text)):
            tab.click()
            break
        
login(browser)
iterate_through_tabs_and_click(browser, desired_class)

time.sleep(10000)





