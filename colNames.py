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

modelColsToKeep = [
        'URN',
        'Stuck',
        'Boarders (name)',
        'OfficialSixthForm (name)',
        'Gender (name)',
    'GOR (name)',
    'Total revenue balance (1) as a % of total revenue income (6) 2017-18',
    'Total revenue balance (1) 2017-18',
    'TotalRevBalance Change 7yr',
    'TotalRevBalance Change 4yr',
    'TotalRevBalance Change 2yr',
    'TOTPUPS__18',
    'PBELIG__18',
    'PGELIG__18',
    'PTKS1GROUP_L__18',
    'PTKS1GROUP_M__18',
    'PTKS1GROUP_H__18',
    'PTFSM6CLA1A__18',
    'PTEALGRP2__18',
    'PTMOBN__18',
    'PSENELSE__18',
    'PNUMEAL',
    'PNUMFSM',
    'PERCTOT',
    'MINORGROUP',
    'ISPRIMARY',
    'ISSECONDARY',
    'ISPOST16',
    'AGEL',
    'AGEH',
    'Pupil:     Teacher Ratio',
    'Mean Gross FTE Salary of All Teachers (Â£s)'
        ]