import time
from selenium import webdriver
import os
from dotenv import load_dotenv
from functions import click_in_dropdown 

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

assignment_num = input("Enter an assignment number: ")

browser = webdriver.Chrome("C:\\bin\\chromedriver.exe")

browser.get("https://learn.zybooks.com/signin")

email = browser.find_element_by_id("ember10")
password = browser.find_element_by_id("ember12")
submit_auth = browser.find_element_by_class_name("title")

email.send_keys(EMAIL)
password.send_keys(PASSWORD)
submit_auth.click()

time.sleep(2)
browser.get("https://learn.zybooks.com/zybook/PLUCSCI144CaoSpring2021")
time.sleep(2)

assignments_tab = browser.find_elements_by_class_name("full-tab")[-1]

assignments_tab.click()

report_button = browser.find_element_by_xpath('//*[@id="ember176"]/div[1]/div[2]/button')
report_button.click()

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

download_assignment_report_button = browser.find_elements_by_class_name("zb-button")
for i in download_assignment_report_button:
    if (i.text == 'Download assignment report'):
        i.click()
        break

time.sleep(100000)

browser.quit()