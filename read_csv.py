import csv
import os
from dotenv import load_dotenv

load_dotenv()

PATH = os.getenv("ASSIGNMENTS_PATH")

assignments = os.listdir(PATH)
assignment_path = PATH + '\\' + assignments[0]

students_and_grades = {}

with open(assignment_path, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        if row[0] == "Last name": continue # Skip the first headers
        full_name = row[0] + ", " + row[1]
        students_and_grades[full_name] = row[6]

print(students_and_grades)