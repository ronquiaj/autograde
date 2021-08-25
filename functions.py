import re

assignment_regex = re.compile('(Week [0-9] Assignment)|Week [0-9]+ - Assignment', re.IGNORECASE)
num_regex = re.compile('\d+')

"""
Function that takes in the drop down options, and the desired option from that drop down. Will click this option from the dropdown.
The regex comparison that is performed looks for the Assignment (1-12), and compares those options in the drop_down_options to our desired which is a number
param: drop_down_options - Selenium[] 
param: desired - number
"""
def click_in_dropdown(drop_down_options, desired):
    for option in drop_down_options:
        if (assignment_regex.match(option.text)):
            parsed_assignment_num = num_regex.search(option.text).group(0)
            if (parsed_assignment_num == desired):
                option.click()
                break