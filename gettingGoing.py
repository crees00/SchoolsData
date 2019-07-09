# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 09:46:13 2019

@author: reesc1
#"""
#import pandas as pd
#
#fileName = r"C:\\Users\\reesc1\\Docs\\Data\\Copy of Management_information_-_schools_-_1_Sept_2005_to_31_August_2015.csv"
#
#df = pd.read_csv(fileName, header=1,encoding='latin-1')


import pandas as pd

folderPath = r"C:\Users\reesc1\Docs\Data"
fileName = folderPath + r"\Copy of Management_information_-_schools_-_1_Sept_2005_to_31_August_2015.xlsx"
df = pd.read_excel(fileName, header=1)
df.to_csv('tester.csv')

#  AP6tmsDdrzYhFLfYu1NGbGB4DAF