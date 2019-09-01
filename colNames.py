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
 ['PSENELSE','PSENELS','PSENSE4','PSENAPS4'],
# ['ATT8SCR', 'PTRWM_EXP','PTAC5EM_PTQ','PTREADWRITTAMATX'],  PROBLEM - ATT8SCR IS NOT A PERCENTAGE BUT IS BEING TREATED LIKE ONE
 ['P8MEA','B8VAMEA_PTQ', 'OVAMEAS'],# Only for ks4
 ['PTL2BASICS_94','PTL2BASICS_LL_PTQ_EE', 'PTL2BASICS_PTQ']] # Only for ks4

Perfks4ColsToKeep = []

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

swfColsToKeep = [ # ~20,000 entries for each
        ["URN"],
        ['Pupil:     Teacher Ratio', 'RATPUPTEA'],
        ['Mean Gross FTE Salary of All Teachers (£s)','Mean Gross FTE Salary of All Teachers (£s)',
         'Mean Gross FTE Salary of All Teachers (Â£s)', 'Mean Gross FTE Salary of All Teachers','SALARY']
        ]
        
cfrColsToKeep = [ # ~13,000 entries for each - missing academy info
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

sfbColsToKeep = [
        ['URN'],
        ['No Pupils'],
        ['% of pupils eligible for FSM'],
        ['Grant Funding'],
        ['Self Generated Funding'],
        ['Teaching staff'],
        ['Supply teaching staff'],
        ['Education support staff'],
        ['Premises'],
        ['Learning resources (not ICT equipment)'],
        ['Brought in Professional Services'],
        ['Total Expenditure']
        ]

fin18list = ['LAESTAB', 'Grant.2018', 'Self.Income.2018',
       'Total.Income.pp.2018', 'Teaching.Staff.2018', 'Supply.Staff.2018',
       'Ed.Support.Staff.2018', 'Premises.2018', 'Back.Office.2018',
       'Catering.2018', 'Other.Staff.2018', 'Energy.2018',
       'Learning.Resources.2018', 'ICT.2018', 'Consultancy.2018', 'Other.2018',
       'Total.Spend.pp.2018']

fin17list=['LAESTAB','Back.Office.2013', 'Back.Office.2014',
       'Back.Office.2015', 'Back.Office.2016', 'Back.Office.2017',
       'Catering.2013', 'Catering.2014', 'Catering.2015', 'Catering.2016',
       'Catering.2017', 'Consultancy.2013', 'Consultancy.2014',
       'Consultancy.2015', 'Consultancy.2016', 'Consultancy.2017',
       'Ed.Support.Staff.2013', 'Ed.Support.Staff.2014',
       'Ed.Support.Staff.2015', 'Ed.Support.Staff.2016',
       'Ed.Support.Staff.2017', 'Energy.2013', 'Energy.2014', 'Energy.2015',
       'Energy.2016', 'Energy.2017', 'Grant.2013', 'Grant.2014', 'Grant.2015',
       'Grant.2016', 'Grant.2017', 'ICT.2013', 'ICT.2014', 'ICT.2015',
       'ICT.2016', 'ICT.2017', 'Learning.Resources.2013',
       'Learning.Resources.2014', 'Learning.Resources.2015',
       'Learning.Resources.2016', 'Learning.Resources.2017', 'Other.2013',
       'Other.2014', 'Other.2015', 'Other.2016', 'Other.2017',
       'Other.Staff.2013', 'Other.Staff.2014', 'Other.Staff.2015',
       'Other.Staff.2016', 'Other.Staff.2017', 'Premises.2013',
       'Premises.2014', 'Premises.2015', 'Premises.2016', 'Premises.2017',
        'Self.Income.2013', 'Self.Income.2014',
       'Self.Income.2015', 'Self.Income.2016', 'Self.Income.2017',
       'Supply.Staff.2013', 'Supply.Staff.2014', 'Supply.Staff.2015',
       'Supply.Staff.2016', 'Supply.Staff.2017', 'Teaching.Staff.2013',
       'Teaching.Staff.2014', 'Teaching.Staff.2015', 'Teaching.Staff.2016',
       'Teaching.Staff.2017', 'Total.Income.pp.2013', 'Total.Income.pp.2014',
       'Total.Income.pp.2015', 'Total.Income.pp.2016', 'Total.Income.pp.2017',
       'Total.Spend.pp.2013', 'Total.Spend.pp.2014', 'Total.Spend.pp.2015',
       'Total.Spend.pp.2016', 'Total.Spend.pp.2017']
       
fin18ColsToKeep = [[x] for x in fin18list]
fin17ColsToKeep = [[x] for x in fin17list]


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
#    'PBELIG__18', only 77% full
#    'PGELIG__18', only 77% full
    'PTKS1GROUP_L__18',
    'PTKS1GROUP_M__18',
    'PTKS1GROUP_H__18',
    'PTFSM6CLA1A__18',
#    'PTEALGRP2__18', # Less than the other EAL one
    'PTMOBN__18',
    'PSENELSE__18',
    'PerformancePctRank', # New col
#    'PTRWM_EXP__18',
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
    'Mean Gross FTE Salary of All Teachers (Â£s)',
    'Grant',
'Self.Income_2yrDiff',
'Total.Income.pp_2yrDiff',
'Teaching.Staff_2yrDiff',
'Supply.Staff_2yrDiff',
'Ed.Support.Staff_2yrDiff',
'Premises_2yrDiff',
'Back.Office_2yrDiff',
'Catering_2yrDiff',
'Other.Staff_2yrDiff',
'Energy_2yrDiff',
'Learning.Resources_2yrDiff',
'ICT_2yrDiff',
'Consultancy_2yrDiff',
'Other_2yrDiff',
'Total.Spend.pp_2yrDiff',

'Self.Income_4yrDiff',
'Total.Income.pp_4yrDiff',
'Teaching.Staff_4yrDiff',
'Supply.Staff_4yrDiff',
'Ed.Support.Staff_4yrDiff',
'Premises_4yrDiff',
'Back.Office_4yrDiff',
'Catering_4yrDiff',
'Other.Staff_4yrDiff',
'Energy_4yrDiff',
'Learning.Resources_4yrDiff',
'ICT_4yrDiff',
'Consultancy_4yrDiff',
'Other_4yrDiff',
'Total.Spend.pp_4yrDiff',

'Self.Income.2018',
'Total.Income.pp.2018',
'Teaching.Staff.2018',
'Supply.Staff.2018',
'Ed.Support.Staff.2018',
'Premises.2018',
'Back.Office.2018',
'Catering.2018',
'Other.Staff.2018',
'Energy.2018',
'Learning.Resources.2018',
'ICT.2018',
'Consultancy.2018',
'Other.2018',
'Total.Spend.pp.2018',
        ]