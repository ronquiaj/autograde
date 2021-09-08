#!/bin/bash

read -p 'Class 1: ' class1
read -p 'Class 2: ' class2

read -p 'Assignment for class 1: ' assignment1
read -p 'Assignment for class 2: ' assignment2

python autograde.py $class1 $assignment1 "https://learn.zybooks.com/zybook/PLUCSCI144CaoSpring2021" & 
python autograde.py $class2 $assignment2 "https://learn.zybooks.com/zybook/PLUCSCI144CaoSpring2021" &