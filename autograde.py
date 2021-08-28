import time
from selenium import webdriver
import os
from dotenv import load_dotenv
from functions import click_in_dropdown 
from read_csv import get_grades

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
PATH = os.getenv("ASSIGNMENTS_PATH")

assignment_num = input("Enter an assignment number: ")

# Configure download path
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--start-maximized")
prefs = {"download.default_directory" : PATH}
chromeOptions.add_experimental_option("prefs", prefs)

browser = webdriver.Chrome("C:\\bin\\chromedriver.exe", options=chromeOptions)

"""
Function which goes to and logs in to Zybooks with provided credentials
"""
def login_to_zybooks(browser):
    browser.get("https://learn.zybooks.com/signin")

    email = browser.find_element_by_id("ember10")
    password = browser.find_element_by_id("ember12")
    submit_auth = browser.find_element_by_class_name("title")
    
    email.send_keys(EMAIL)
    password.send_keys(PASSWORD)
    submit_auth.click()

"""
Goes to the assignments tab, clicks on the report button
"""
def navigate_to_dropdown_window(browser):
    browser.get("https://learn.zybooks.com/zybook/PLUCSCI144CaoSpring2021")
    time.sleep(2)
    assignments_tab = browser.find_elements_by_class_name("full-tab")[-1]
    assignments_tab.click()
    time.sleep(2)
    report_button = browser.find_element_by_xpath('//*[@id="ember176"]/div[1]/div[2]/button')
    report_button.click()

"""
Configures the dropdowns to match the desired class, and specifies that we want the second section of this class
"""
def configure_dropdowns(browser):
    dropdowns = browser.find_elements_by_class_name("ember-basic-dropdown-trigger")
    browser.implicitly_wait(2)
    topics = dropdowns[0]
    students = dropdowns[1]
    
    topics.click()
    first_drop_down_options = browser.find_elements_by_class_name("ember-power-select-option")
    click_in_dropdown(first_drop_down_options, assignment_num)

    students.click()
    section2 = browser.find_elements_by_class_name("ember-power-select-option")[2]
    section2.click()

"""
Finds the download button and clicks download
"""
def download_csv(browser):
    download_assignment_report_button = browser.find_elements_by_class_name("zb-button")
    for i in download_assignment_report_button:
        if (i.text == 'Download assignment report'):
            i.click()
            break

login_to_zybooks(browser)
time.sleep(2)
navigate_to_dropdown_window(browser)
time.sleep(2)
configure_dropdowns(browser)
time.sleep(2)
download_csv(browser)
time.sleep(3)
print(get_grades(assignment_num))










time.sleep(100000)

browser.quit()