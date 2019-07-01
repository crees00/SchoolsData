# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
import re

folderPath = r"C:\Users\Chris\Documents\Documents\ONS\\" 

def initialiseVariables():
    global ratingsDict
    global currentRatingsDict
    global oldURNs
    global URNsNotIndf0
    global stuck
    global subbedTheSub
    global allPreds, allParents
    allParents = []
    dictsAndLists = {'ratingsDict':{}, 'currentRatingsDict':{},
                     'oldURNs':[], 'URNsNotIndf0':[], 'subbedTheSub':[],
                     'stuck':[], 'allPreds':[], 'allParents':[]}
    return dictsAndLists

def loadData(fileName):
    global df0
    df0 = pd.read_csv(folderPath + fileName)
    print('\nData loaded!')
    return df0

def addRatingToDict(row, params):
    ''' Look up overall effectiveness rating for that row.
    Add it to the tally for that URN in the dictionary.
    If overall effectiveness is not 1-4, append it to list in position 0'''
    dictToUse = params['ratingsDict']
    URN = row['URN']
    cat = row['Overall effectiveness']
    
    if URN not in dictToUse.keys():
        dictToUse[URN] = [[],0,0,0,0] # [random others, cat1, cat2, cat3, cat4]
    try:
        dictToUse[URN][cat] += 1
    except:
        dictToUse[URN][0].insert(0,row['Overall effectiveness'])
    params['ratingsDict'] = dictToUse

def addPreviousRatingsToDict(row, params):
    '''Look up schools/academies that are currently open. See if they have
    any predecessors and add the predecessor scores to those of the current
    school/academy.
    Dictionary contains an entry for each school/academy that has been
    inspected since 2005 - regardless of whether it is open or closed.
    '''
    pred = row['Predecessor School URN(s)']
    predList = re.findall('[0-9]{4,7}',str(pred))
    
    if len(predList) >0:
        for no in predList:
            no=int(no)
            
            # Check current URN isn't listed as a predecessor
            if no==row['URN']:
                continue
            params['allPreds'].append(no)
            params['allParents'].append(row['URN'])
            params = addPredRatings(row['URN'],no, params)
            # Add to list of removed URNs so don't double count later
            params['oldURNs'].append((row['URN'],no))
        

def addPredRatings(currURN, oldURN, params):
    '''Add the inspection ratings under the old URN to the inspection
    ratings for the current URN
    Just updates the currentRatingsDict dictionary
    '''
    ratingsDict, currentRatingsDict = params['ratingsDict'], params['currentRatingsDict']
    if currURN == oldURN:
        print('currURN == oldURN for', currURN)
        return
    
    # Check oldURN is in the URN column
    if (int(oldURN) in ratingsDict.keys()):
        # Check not double counting as multiple rows will have same URN combo
        if (currURN,oldURN) not in params['oldURNs']:
            try:
                if len(ratingsDict[oldURN][0])>0:
                    currentRatingsDict[currURN][0].append(ratingsDict[oldURN][0])
                for cat in range(1,5):
                    currentRatingsDict[currURN][cat] += ratingsDict[oldURN][cat]
            except KeyError:
                params['subbedTheSub'].append(currURN)
    else:
        # If previous URN is not in df0 then assume that previous URN
        # has not been inspected since 2005 so has nothing to add
        params['URNsNotIndf0'].append(oldURN)
    
    return params

def stuckURN(URN, dictToUse, params):
    '''Looks up the given URN in the given dictionary, calculates
    whether the school is stuck and, if so, adds it to stuck list'''
    ratings = dictToUse[URN]
    if len(ratings[0]) + ratings[1] + ratings[2] + ratings[3] + ratings[4] >=4:
        if  ratings[1] + ratings[2] ==0:
            params['stuck'].append(URN)
    return params['stuck']
        
def stuckDict(dictToUse, params):
    '''Applies stuckURN to each URN in the given dictionary'''
    print('Identifying stuck schools...')
    for URN in dictToUse:
        stuckURN(URN, dictToUse, params)
    print(len(params['stuck']),'items in stuck')
    return params['stuck']

def addStuckCol(df, params, write=False):
    '''Add a column called Stuck to the df
    1 if the URN is in the 'stuck' list
    0 if not stuck
    If write != False then write to .csv
    '''
    print('Adding/updating stuck column in df...')
    df['Stuck'] = df.apply(lambda row: np.where(
            (int(row['URN']) in params['stuck']),1,0), axis=1)
    if write:
        print('Writing .csv file...')
        df.to_csv('allDataWithStuck.csv')
    return df

def dropCols(df):
    '''Removes all the columns in the big list from the df'''
    print('Dropping unneeded cols...')
    toDrop = ['Unnamed: 0',
 'Web link',
 'Inspection number',
 'Inspection type',
 'Academic year',
 'Inspection start date',
 'Inspection end date',
 'First published date',
 'Latest published date',
 'Overall effectiveness',
 'Sixth form provision',
 'Early years provision',
 "Pupils' achievement (aggregated)",
 'Achievement of pupils',
 'How well do pupils achieve?',
 'Behaviour and safety of pupils',
 'Quality of teaching',
 'Leadership and management',
 'Overall effectiveness of residential experience (aggregated)',
 'The effectiveness of the boarding provision (pre Jan 2012)',
 'Overall effectiveness of residential experience (post Jan 2012)',
 'Outcomes for residential pupils (post Jan 2012)',
 'Quality of residential provision and care (post Jan 2012)',
 'Residential pupils safety (post Jan 2012)',
 'Leadership and management of the residential provision (post Jan 2012)',
 'The effectiveness of partnerships in promoting learning and well-being',
 "The school's capacity for sustained improvement",
 'Outcomes for individuals and groups of pupils',
 "Pupils' attainment",
 "The quality of pupils' learning and their progress",
 'Outcomes for children in the Early Years Foundation Stage',
 'The quality of learning for pupils with special educational needs and/or disabilities and their progress',
 'Outcomes for students in the sixth form ',
 "The extent of pupils' spiritual, moral, social and cultural development",
 'The extent to which pupils adopt healthy lifestyles',
 'The extent to which pupils feel safe',
 "Pupils' attendance",
 'The extent to which pupils contribute to the school and wider community',
 'The extent to which pupils develop workplace and other skills that will contribute to their future economic well-being',
 'The quality of provision in the sixth form',
 "The extent to which the curriculum meets pupils' needs, including, where relevant, through partnerships",
 'The effectiveness of care, guidance and support',
 'The use of assessment to support learning',
 'The quality of provision in the Early Years Foundation Stage',
 'The effectiveness of leadership and management of the Early Years Foundation Stage',
 'The effectiveness of leadership and management of the sixth form',
 'The effectiveness with which the school promotes equality of opportunity and tackles discrimination',
 'The effectiveness with which the school promotes community cohesion',
 'The effectiveness with which the school deploys resources to achieve value for money',
 'The effectiveness of the governing body in challenging and supporting the school so that weaknesses are tackled decisively...',
 'The effectiveness of safeguarding procedures',
 "The effectiveness of the school's engagement with parents and carers",
 'The leadership and management of teaching and learning',
 "Pilot_Does the school adequately promote the pupils' well-being?",
 'Pilot_Does the school adequately promote community cohesion?',
 'Pilot_Does the school provide value for money?',
 'Inspection number of the previous inspection',
 'Academic year of the previous inspection',
 'Inspection end date of the previous inspection',
 'Previous inspection - Overall effectiveness',
 'Previous inspection - Category',
 'Movement in overall effectiveness since previous inspection',
 'Time between inspections (months)',
 'Web Link',
 'Inspection type grouping',
 'Event type grouping',
 'Category of concern',
 'Outcomes for pupils',
 'Quality of teaching, learning and assessment',
 'Effectiveness of leadership and management',
 'Personal development, behaviour and welfare',
 'Early years provision (where applicable)',
 '16 - 19 study programmes',
 'Previous inspection number',
 'Previous inspection start date',
 'Previous inspection end date',
 'Previous overall effectiveness',
 'Previous category of concern',
 'Previous outcomes for pupils',
 'Previous quality of teaching, learning and assessment',
 'Previous effectiveness of leadership and management',
 'Previous personal development, behaviour and welfare',
 'Previous early years provision (where applicable)',
 'Previous 16 - 19 study programmes',
 'Number of warning notices issued in 2016/17 academic year',
 'Publication date',
 'Previous publication date',
 'Outcomes for short inspections that did not convert',
 'Does the previous inspection relate to the school in its current form?',
 'URN at time of previous inspection',
 'LAESTAB at time of previous inspection',
 'School name at time of previous inspection',
 'School type at time of previous inspection',
 'Inspection type grouping (final)',
 '16-19 study programmes',
 'Previous 16-19 study programmes',
 'Linked school type of education',
 'OB number on Roll',
 'conversion decision',
 'deemed flag',
 'Withdrawn date',
 'Previous withdrawn date']
    df.drop(toDrop, axis=1,inplace=True)
    return df

def generateDFs(df, write=False):
    ''' Takes a df and generates a new df with one row for each URN.
    For each URN, finds the most recent (non-blank) data for each column
    and puts this into the row for that URN. Then merges each row into 
    a new df and outputs to .csv file.
    '''
    print('Making df with a row for each school...')
    URNs = set(df['URN'])
    listOfRows = []
    for URN in URNs:
        if (100*len(listOfRows)/len(URNs))%5 ==0:
            print(100*len(listOfRows)/len(URNs),'% done')
        minidf = df[df['URN']==URN].copy()
        
        # Work through all rows with same URN
        currRow = minidf.iloc[0,:].copy()
        for rowNo in range(len(minidf)):
            row = minidf.iloc[rowNo,:].copy()
            mask = ~row.isnull()
            currRow[mask] = row[mask]
        listOfRows.append(currRow)
    dfByURN = pd.DataFrame(listOfRows, columns=listOfRows[0].index)
    if write:
        print('Writing .csv file...')
        dfByURN.to_csv('dfByURN.csv')
    return dfByURN

def removeClosedSchools(params, df=False, write=False):
    ''' Removes schools that don't have a URN in the edubase openSchools file.
    Can either be sent a df or will default to reading in dfByURN.csv and 
    returns the reduced df.
    '''
    print('Removing closed schools...')
    if type(df)==bool:
        df = pd.read_csv(folderPath + 'dfByURN.csv') 
    openSchools = pd.read_csv(folderPath + 
          'edubaseallstatefunded20190627.csv',
                              encoding='latin-1')
    a,params['openSchoolsSet'] = set(df['URN']), set(openSchools['URN'])
    b = params['openSchoolsSet']
    c = set(params['ratingsDict'].keys())
    print(len(a), 'dfByURN no of URNs')
    print(len(b), 'openSchools no of URNs')
    print(len(a-b),'schools in dfByURN that are not actually open')
    print(len(b-a),'open schools that are not in dfByURN that should be\n\
          or just have not been inspected in the time period')
    print(len(b&a),'schools in dfByURN and openSchools so should appear in final df')
    print(len(c&b), 'schools in ratingsDict and openSchools')

    dfOnlyOpen = df.merge(openSchools[['URN', 'HeadLastName']],
                               how='inner', on='URN')
    dfOnlyOpen.drop(['HeadLastName'], axis=1, inplace=True)
    print(dfOnlyOpen.shape,'shape of dfOnlyOpen')
    print(len(dfOnlyOpen['URN']),'schools in dfOnlyOpen')
    if write:
        dfOnlyOpen.to_csv('dfOnlyOpen')
    return dfOnlyOpen, params

def countBlanks(df, write=False):
    ''' Used to check if the generateDFs function has worked properly.
    For each URN, generates a row in a new df with true/false values.
    True: All values for that URN in that column are blank
    False: There is at least one non-blank value for that URN in that column
    
    Can then compare with the dfbyURN.csv file - if there is a False where
    there is a blank in the dfByURN.csv file, generateDFs hasn't picked up
    the non-blank value
    '''
    URNs = set(df['URN'])
    global rows
    rows=[]
    row = df.iloc[0,:].copy()
    counter=5
    for URN in URNs:
        if (100*len(rows)/len(URNs)) > counter:
            print((100*len(rows)/len(URNs))//1,'% done')
            counter += 5
        minidf = df[df['URN']==URN].copy()
        
        # count no of blanks in each col
        for col in (set(minidf.columns)-set(['URN'])):
            # True if all values are blank
            row[col] = (len(minidf) == len(minidf[minidf[col].isnull()]))
        row['URN'] = URN
        rows.append(row.copy())
    global showBlanks
    showBlanks = pd.DataFrame(rows, columns = rows[0].index)
    print('Writing .csv file...')
    showBlanks.to_csv('showBlanks.csv')
#countBlanks(df0)

