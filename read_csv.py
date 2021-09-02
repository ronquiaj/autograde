import csv
import os
import re
from dotenv import load_dotenv

load_dotenv()

PATH = os.getenv("ASSIGNMENTS_PATH")
assignment_regex = re.compile('(?<=Week_)[0-9]+', re.IGNORECASE)

"""
Function which uses regex to find the corresponding assignment against our assignment number, returns the path to that assignment
"""
def get_assignment_path(assignment_num):
    assignments = os.listdir(PATH)
    for assignment in assignments:
        num = assignment_regex.search(assignment).group(0) # Use the regex to get the assignment number for this file
        if str(num) == str(assignment_num):
            return assignment
    raise ValueError("Assignment was not found, please try again")
            
    

"""
Given an assignment number, looks through our assignments folder and finds the corresponding csv. Builds an object containing students mapped to their grades for that week
"""
def get_grades(assignment_num):
    assignment_path = PATH + "\\" + get_assignment_path(assignment_num)
    students_and_grades = {}

    with open(assignment_path, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            if row[0] == "Last name": continue # Skip the first headers
            last_name = row[0].lower()
            # first_name = row[1]
            full_name = last_name
            students_and_grades[full_name] = row[6]

    return students_and_grades
