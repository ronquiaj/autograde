#!/bin/bash

read -p 'Assignment for CSCI 144 Section 2: ' assignment1
read -p 'Assignment for CSCI 144 Section 3: ' assignment2

python autograde.py "CS144 Introduction to Computer Science Fall2021" $assignment1 "https://learn.zybooks.com/zybook/PLUCSCI144Fall2021" 2 & 
python autograde.py "CS 144 - 03 Fall 2021" $assignment2 "https://learn.zybooks.com/zybook/PLUCSCI144Fall2021" 3 &