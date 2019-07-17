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

AbsenceColsToKeep = [
        'URN',
        'PERCTOT',
  #      'PPERSABS10'
        ]

SpineColsToKeep = [
        'URN',
        'MINORGROUP',
        'NFTYPE',
        'ISPRIMARY',
        'ISSECONDARY',
        'ISPOST16',
        'AGEL',
        'AGEH',
        'GENDER'
        ]

swfColsToKeep = [
        ["URN"],
        ['Pupil:     Teacher Ratio', 'RATPUPTEA'],
        ['Mean Gross FTE Salary of All Teachers (£s)','Mean Gross FTE Salary of All Teachers (£s)',
         'Mean Gross FTE Salary of All Teachers (Â£s)', 'Mean Gross FTE Salary of All Teachers','SALARY']
        ]
        
cfrColsToKeep = [
        ['URN'],
        ['PUPILS'],
        ['FSM'],
        ['GRANTFUNDING'],
        ['SELFGENERATEDINCOME'],
        ['TEACHINGSTAFF'],
        ['SUPPLYTEACHERS'],
        ['EDUCATIONSUPPORTSTAFF'],
        ['PREMISES'],
        ['LEARNINGRESOURCES'],
        ['BOUGHTINPROFESSIONALSERVICES'],
        ['TOTALEXPENDITURE'],
        ['DCAT1'],
        ['DCAT2'],
        ['DCAT5'],
        ['PTEACHINGSTAFF']        
        ]
bla=[]
for colList in cfrColsToKeep:
    bla.append(colList[0])
print(bla)