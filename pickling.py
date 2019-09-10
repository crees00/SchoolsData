# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 10:14:39 2019

@author: Chris
"""

#import os
#
#currentFolder = os.path.dirname(os.path.abspath(__file__))
#print('currentFolder:',currentFolder)

import setFolder as sf
import dill
def save_dill(obj, name):
    '''Puts the path in for you'''
    with open(sf.addFolderPath(name + '.pik'), 'wb') as f:
        dill.dump(obj, f)
    print('pickled')

def load_dill(name):
    '''Doesn't do the path'''
    try:
        with open(name , 'rb') as f:
            return dill.load(f)
    except FileNotFoundError:
        with open(sf.addFolderPath(name), 'rb') as f:
            return dill.load(f)
#if __name__ == "__main__":
#    save_dill(modelDict, 'modelDictAllFeatures0908')
#    aReloaded = load_dill('modelDictWithDill')
#    pass