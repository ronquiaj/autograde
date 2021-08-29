

import time
from selenium import webdriver
import os
from dotenv import load_dotenv
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

load_dotenv()
SAKAI_USERNAME = os.getenv("SAKAI_USERNAME")
SAKAI_PASSWORD = os.getenv("SAKAI_PASSWORD")

desired_class = input("Enter the name of the class you'd like to click on: ")
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--start-maximized")
browser = webdriver.Chrome("C:\\bin\\chromedriver.exe", options=chromeOptions)

"""
Logs in to Sakai through the guest route.
"""
def login(browser):
   
    browser.get("https://sakai.plu.edu/portal")

    guest_login_button = browser.find_element_by_id("loginLink2")
    guest_login_button.click()
    
    time.sleep(3)

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

    time.sleep(2)
    column_headers = browser.find_elements_by_class_name("gb-title")
    time.sleep(2)
    assignment_index = 0
    cur_index = 0
    for column_header in column_headers:
        assignment = column_header.get_attribute("title")
        if ("Assign" in assignment):
            if (str(assignment_num) in assignment): # Find the column of the assignment we are looking for
                assignment_index = cur_index
                break
            else:
                cur_index += 1
       

    rows = browser.find_elements_by_css_selector("tr")
    time.sleep(2)
    c = 0
    for row in rows:
        columns = row.find_elements_by_css_selector("div.relative > span.gb-value")
        try:
            if (len(columns) > 0):
                grade_cell = columns[assignment_index + 1]
                print("Text:", grade_cell.text, ", Displayed:", grade_cell.is_displayed(), ", Enabled:", grade_cell.is_enabled())
                # ActionChains(browser).move_to_element(grade_cell).perform()
                ActionChains(browser).move_to_element(grade_cell).click(grade_cell).send_keys("100").send_keys(Keys.ENTER).perform()
                if (c == 5):
                  break
                c += 1
           
        except IndexError:
            break
    print("Done")
        

login(browser)
iterate_through_tabs_and_click(browser, desired_class)
time.sleep(2)
click_on_gradebook(browser)
time.sleep(2)

iterate_through_students(browser, 2)
time.sleep(10000)







