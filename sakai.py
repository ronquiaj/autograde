

import time
from selenium import webdriver
import os
from dotenv import load_dotenv
import re
from selenium.webdriver.common.action_chains import ActionChains

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

def click_on_gradebook(browser):
    tab = browser.find_element_by_class_name("icon-sakai--sakai-gradebookng")
    tab.click()
    
def iterate_through_students(browser, assignment_num):
    view_columns_button = browser.find_element_by_id("toggleGradeItemsToolbarItem")
    view_columns_button.click()
    
    hide_all_button = browser.find_element_by_id("hideAllGradeItems")
    hide_all_button.click()
    
    filter_items = browser.find_elements_by_class_name("gb-item-filter")
    for filter_item in filter_items:
        if "Assign" in filter_item.text:
            filter_item.click()
    
    gradeTable = browser.find_element_by_id("gradeTable")
    gradeTable.click()
    
    browser.execute_script("document.querySelector('.wtHolder').scrollBy(2000, 1000)")

    time.sleep(3)
    column_headers = browser.find_elements_by_class_name("gb-title")
    header_index = 0
    for column_header in column_headers:
        assignment = column_header.get_attribute("title")
        if column_header.is_displayed():
           if (str(assignment_num) in assignment):
               print(assignment)
    
    # Get rows
    rows = browser.find_elements_by_css_selector("tr")
    for row in rows:
        columns = row.find_elements_by_css_selector("td")
        for column in columns:
            print(column.text)
        

login(browser)
iterate_through_tabs_and_click(browser, desired_class)
time.sleep(2)
click_on_gradebook(browser)
time.sleep(2)

iterate_through_students(browser, 2)
time.sleep(10000)







