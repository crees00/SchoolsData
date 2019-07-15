# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 14:28:48 2019

@author: reesc1
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 18:48:13 2019

@author: Chris
"""

import pandas as pd
import numpy as np
import setFolder as sf
import colNames as cn
import creatingAMonster as cam
import datetime
import findStuck
import copy

start = datetime.datetime.now()
print(f"running censusData at {start}")


def readCensusData():
    censusDF18 = pd.read_csv(
        sf.homeFolder + r"\2017-2018\Absence and Pupil Population\england_census.csv",
        encoding="latin-1",
    )
    return censusDF18
censusDF18 = readCensusData()