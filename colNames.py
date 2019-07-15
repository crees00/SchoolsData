# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 16:34:12 2019

@author: Chris
"""

# to keep from ks2 performance
PerfCols18ks2ToKeep = ['URN','RELDENOM','AGERANGE','TOTPUPS','PBELIG','PGELIG' ,
                     'PTKS1GROUP_L','PTKS1GROUP_M','PTKS1GROUP_H','PTFSM6CLA1A',
                     'PTEALGRP2','PTMOBN','PSENELSE', 'PTRWM_EXP']

PerfCols14ks2ToKeep = {'AGERANGE',
 'PBELIG',
 'PGELIG',
 'RELDENOM',
 'TOTPUPS',
 'URN',
  'PTEALGRP2',
 'PTMOBN',
}

PerfColsToKeep = [['URN'],
 ['RELDENOM'],
 ['AGERANGE'],
 ['TOTPUPS','TPUP1618'],
 ['PBELIG','PBPUP'],
 ['PGELIG','PGPUP'],
 ['PTKS1GROUP_L','PKS1EXP_L','PTPRIORLO'],
 ['PTKS1GROUP_M','PKS1EXP_M','PTPRIORAV'],
 ['PTKS1GROUP_H','PKS1EXP_H','PTPRIORHI'],
 ['PTFSM6CLA1A','PTFSMCLA'],
 ['PTEALGRP2'],
 ['PTMOBN','PTNMOB'],
 ['PSENELSE','PSENELS','PSENSE4','PSENAPS4']]

CensusColsToKeep = [
        'URN',
        'LA',
        'ESTAB',
        ['NOR','TOTPUPSENDN'],
        'PNUMEAL',
        'PNUMFSM']