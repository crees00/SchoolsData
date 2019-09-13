# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 13:00:57 2019

analyse a version of 'modelDict' which is run on just a subset of the best models

each model in modelDict will be one of 5 folds


For each model:
    find the test set
    Identify which URNs are in the test set
    Get the predictions on the training set
    make dictionary with {URN: Prediction} pairs
    
At the end of this loop:
    can save the dict and don't immediately need to keep modelDict
    merge the 5 dictionaries for each model, to have one dict for each model, containing every school in df and its prediction

Now make dict of dicts, with {runName:{URN:pred, URN:pred,...},...}
Can also make confusion matrix for each run

@author: Chris
"""

