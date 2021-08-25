import time
import re
from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

assignment_regex = re.compile('(Week [0-9] Assignment)|Week [0-9]+ - Assignment', re.IGNORECASE)
num_regex = re.compile('\d+')

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

for option in first_drop_down_options:
    if (assignment_regex.match(option.text)):
        parsed_assignment_num = num_regex.search(option.text).group(0)
        if (parsed_assignment_num == assignment_num):
            option.click()



time.sleep(100000)

browser.quit()