

import time
from selenium import webdriver
import os
from dotenv import load_dotenv
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

load_dotenv()

# desired_class = input("Enter the name of the class you'd like to click on: ")
# chromeOptions = webdriver.ChromeOptions()
# chromeOptions.add_argument("--start-maximized")
# browser = webdriver.Chrome("C:\\bin\\chromedriver.exe", options=chromeOptions)

"""
Logs in to Sakai through the guest route.
"""
def login(browser, USERNAME, PASSWORD):
   
    browser.get("https://sakai.plu.edu/portal")

    guest_login_button = browser.find_element_by_id("loginLink2")
    guest_login_button.click()
    
    time.sleep(3)

    username = browser.find_element_by_id("eid")
    password = browser.find_element_by_id("pw")
    submit_login_button = browser.find_element_by_id("submit")

    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)
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

"""
Clicks on the gradebook tab on Sakai
"""
def click_on_gradebook(browser):
    tab = browser.find_element_by_class_name("icon-sakai--sakai-gradebookng")
    tab.click()

"""
Filters out anything that isn't assignment related
"""
def filter(browser):
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

"""
Function which iterates through the assignment headers, and returns the index of the assignment we want to grade for each student
"""
def get_assignment_index(browser, assignment_num):
    browser.execute_script("document.querySelector('.wtHolder').scrollBy(2000, 1000)") # Used so we can load all of the table data
    column_headers = browser.find_elements_by_class_name("gb-title")
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
    return assignment_index

"""
Using the found assignment index, finds the column to grade each student row, and puts in the grade from the provided dictionary
"""
def grade_students(browser, assignment_num, students_to_grades):
    assignment_index = get_assignment_index(browser, assignment_num)
    rows = browser.find_elements_by_css_selector("tr")
    for row in rows:
        columns = row.find_elements_by_css_selector("div.relative > span.gb-value")
        try:
            if (len(columns) > 0):
                # first_name = row.find_element_by_class_name("gb-first-name").text
                last_name = row.find_element_by_class_name("gb-last-name").text
                full_name = last_name.lower()
                student_grade = 0
                print(full_name)
                try:
                    student_grade = students_to_grades[full_name]
                except KeyError:
                    print("Descrepancy for student", full_name, "- Student most likely has name that differs from Sakai to Zybooks")
                    continue
                print(full_name, ":", student_grade)
                grade_cell = columns[assignment_index + 1]
                ActionChains(browser).click(grade_cell).send_keys(student_grade).send_keys(Keys.ENTER).perform()
                time.sleep(1)
        except IndexError:
            break
    print("Done")
        
def grade(browser, desired_class, assignment_num, students_to_grades):
    SAKAI_USERNAME = os.getenv("SAKAI_USERNAME")
    SAKAI_PASSWORD = os.getenv("SAKAI_PASSWORD")
    login(browser, SAKAI_USERNAME, SAKAI_PASSWORD)
    iterate_through_tabs_and_click(browser, desired_class)
    time.sleep(2)
    click_on_gradebook(browser)
    time.sleep(2)
    filter(browser)
    time.sleep(2)
    grade_students(browser, assignment_num, students_to_grades)









