# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 10:14:39 2019

@author: Chris
"""
#import os
#
#currentFolder = os.path.dirname(os.path.abspath(__file__))
#print('currentFolder:',currentFolder)


import dill
def save_dill(obj, name):
    with open(name + '.pik', 'wb') as f:
        dill.dump(obj, f)

def load_dill(name):
    with open(name + '.pik', 'rb') as f:
        return dill.load(f)

if __name__ == "__main__":
    save_dill(modelDict, 'modelDictAllFeatures0908')
#    aReloaded = load_dill('modelDictWithDill')
#    pass