# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 14:38:24 2019

@author: reesc1
"""
import pandas as pd

class school():
    def __init__(self,URN):
        self.URN = URN
        self.inspDict = {1:[], 2:[], 3:[], 4:[], 9:[], 'nums':[]}
        
        
        
class inspection():
    def __init__(self, inspNo, cat, URN):
        self.URN = URN
#        self.date = date
        self.cat = cat
        self.inspNo = inspNo



def loadInspections(row):
    inspection(str(row['Inspection number']),row['Overall effectiveness'],row['URN'])

df = pd.read_csv('bigDFnoDups1.csv')

df = df.apply(loadInspections, axis=1)
