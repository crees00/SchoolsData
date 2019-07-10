# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 11:30:33 2019

@author: reesc1
"""
import os

folderPath = r"Y:\2. Education, Skills, Children's Social Care\Ofsted - Stuck Schools\2. Data\1. Raw Data\Schools Data Files - 2005-present\DfE Data"


folders = {}
subfolders = []

for folder in os.listdir(folderPath):
    folders[folder] = {}
    for subfolder in os.listdir(folderPath + "\\" + folder):
        try:
            folders[folder][subfolder] = os.listdir(
                folderPath + "\\" + folder + "\\" + subfolder
            )
            if subfolder not in subfolders:
                subfolders.append(subfolder)
        except NotADirectoryError:
            print(subfolder, "can't be opened")
print("\n\n")
fails = []
foldersReordered = {}
for subfolder in subfolders:
    foldersReordered[subfolder] = {}
    for folder in os.listdir(folderPath):
        try:
            foldersReordered[subfolder][folder] = folders[folder][subfolder]
        except:
            fails.append(
                "subfolder:" + subfolder + ", folder:" + folder + "did not work"
            )

file1 = open("foldersDict.txt", "w")
for key in foldersReordered.keys():
    print(key)
    file1.write(key + "\n")
    for sub in foldersReordered[key].keys():
        print(sub)
        file1.write("\n" + sub + "\n")
        print(foldersReordered[key][sub])
        for item in foldersReordered[key][sub]:
            file1.write(item + "\n")
    print()
    file1.write("\n")
