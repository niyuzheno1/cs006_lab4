# autodirfinder.py --- Find all the dirs to be graded under directory variable
#
# Copyright (C) 2020 Zach (Yuzhe) Ni
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.

import grading
import os
directory = "C:\\Users\\zachn\\OneDrive\\Documents\\labs\\lab4\\tmp"

os.chdir(directory)

text_file = open(directory + "\\result.txt", "w")

def directory_find(root='.'):
    for path, dirs, files in os.walk(root):
        if ".c9" in path:
            continue
        for x in dirs:
            if '4' in x:
                return os.path.join(path, x)

dataofstudents = {'Name' :[] , 'ID': [], 'scores': [], 'comments' : []}
currentlevel = next(os.walk('.'))[1] 
for x in currentlevel:
    try:
        df = directory_find(directory+ "\\{0}\\environment\\".format(x))
        bfl = False 
        if df is None:
            text_file.write(x)
            text_file.write("\n")
        else:
            os.chdir(df)
            grading.main()
            bfl = True  
    except OSError as e:
        text_file.write(x)
        text_file.write("\n")
text_file.close()