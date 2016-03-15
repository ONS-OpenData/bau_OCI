 # -*- coding: utf-8 -*-
"""
Spyder Editor

Developing basic reusable functions to help transforn data with Pandas.

Author: Mike
"""

import pandas as pd


"""
Neatly concatenates columns, also their labels. Changes all to string
"""
def concat_topics(myframe, target, columns, divider):

        for each in columns:
            if myframe[each].dtype == float:
                myframe[each] = myframe[each].astype(str)
            elif myframe[each].dtype == int:
                myframe[each] = myframe[each].astype(str)
                myframe[each] = myframe[each].map(lambda x: x.replace('.0', ''))
            else:
                myframe[each] = myframe[each].astype(str)
                                
        myframe[target] = myframe[target].map(lambda x: x.strip())
        for each in range(1, len(columns)):
            myframe[target] = myframe[target] + divider + myframe[columns[each]].map(lambda x: x.strip())     
        label = 'dimension_item_label_eng_' + str(target[-1:])
        myframe[label] = myframe[target]
        
        return myframe
   

"""
Neatly concatenates columns, also their labels. Changes all to string
"""
def concat_topics_no_repeats(myframe, target, columns, divider):
    # NOT IMPLEMENTED YET
    # Needs to concat items but miss out any repeats    
    pass      

   

"""
Sort out the datatypes. Leave it if its a float. Otherwise if it wont be an int, make ita string
"""
def define_data_types(myframe):
    for each in list(myframe.columns.values):
        if myframe[each].dtype != float:
            try:
                myframe[each] = myframe[each].astype(int)
            except:
                myframe[each] = myframe[each].astype(str)
    return myframe



"""
Set the data types of the columns in the dataframe
"""
def multi_load(loadfiles):
    # Load it in    
    myframe = pd.read_csv(loadfiles[0], dtype = object)
    for x in range(1, len(loadfiles)-1):
        newframe = pd.read_csv(loadfiles[x], dtype = object)
        myframe = pd.concat(myframe, newframe)
        myframe = myframe.reset_index()
        myframe = myframe.drop['index']

    myframe.fillna('', inplace=True)
    myframe = define_data_types(myframe)
    
    # let the user know if there're any loading issues
    if len(loadfiles) != (len([myframe['observation'] == '*********'])+1):
            print 'MISCOUNT OF FILEFOOTERS! ONE OF YOUR CSVS HAS FAILED TO LOAD COMPLETLY' 
            raw_input('press a key to continue')
    
    # Strip the old footer out
    myframe = myframe[myframe['observation'] != '*********']    
    myframe.fillna('', inplace = True)    
    
    # Get any trailing .0'sout of data markings. (Probably a better place for this).
    myframe['data_marking'] = myframe['data_marking'].astype(str)
    myframe['data_marking'] = myframe['data_marking'].map(lambda x: x.replace('.0', ''))
    
    # Add a new footer
    count = len(myframe)
    myframe = myframe.set_value(len(myframe), 'observation', '*********')
    myframe = myframe.set_value(len(myframe) -1, 'data_marking', str(count))
    
    return myframe



"""
The initial load of the CSV file
"""
def single_load(loadfile):
    myframe = pd.read_csv(loadfile, dtype = object)
    myframe.fillna('', inplace = True)
    
    # Get any trailing .0'sout of data markings. (Probably a better place for this).
    myframe['data_marking'] = myframe['data_marking'].astype(str)
    myframe['data_marking'][-1] = myframe['data_marking'].map(lambda x: x.replace('.0', ''))

    return myframe



"""
Overright the current topic dimension numbering with correct numbering
"""
def validateheaders(myframe):
    standard_headings = ['dim_id_', 'dimension_label_eng_', 'dimension_label_cym_', 'dim_item_id_',
                         'dimension_item_label_eng_', 'dimension_item_label_cym_', 'is_total_', 'is_sub_total_']
    for count in range(35, len(myframe.columns.values), 8):
        for x in range(0, 8):
           myframe.rename(columns={myframe.columns[count+x]: standard_headings[x] + str((count-35) / 8 + 1)}, inplace=True)
    return myframe

   
        
"""
A remove command for removing a list of quoted text from a list of columns.
"""
def remove_from_columns(myframe, headers, items):
    
        for each in headers:
            myframe[each] = myframe[each].astype(str)
            for item in items:
                myframe[each] = myframe[each].map(lambda x: x.replace(item, ''))
                myframe[each] = myframe[each].map(str.strip)
        return myframe



"""
Dismiss command for unwanted items. Will remove all 8 relevant columns.
"""
def dismiss(myframe, headers):
    
    for each in headers:
        Column1 = myframe.columns.get_loc(each)
        for x in range(1, 9):
            myframe = myframe.drop(myframe.columns[Column1], axis=1)
        # print 'Dismissed ' + str(each) + ' and associated fields.'
    return myframe
    
"""

EVERYTHING BEYOND THIS POINT DEALS WITH THE DIMENSIONAL COMPARISSON TOOL

Created on Wed Sep 30 12:36:30 2015



@author: Mike

Compares the dimensions and dimension items within a CSV and a Check_file (script of python dictionary functions that retains the same info)

"""

import pandas as pd
import sys
import numpy as np
import check_file as chk


"""
Create a dictionary of unique dimensions and dim items from a given csv 
"""
def create_unique_dict(load_file):
    my_uniques = []
    obs_file = pd.read_csv(load_file)
    obs_file.fillna('', inplace = True)
    all_cols = list(obs_file.columns.values)
    wanted_cols = []
    for each in all_cols:
        if 'dim_item_id_' in each:
            wanted_cols.append(each)
    for each in all_cols:
        if 'dim_id_' in each:
            wanted_cols.append(each)
    for each in wanted_cols:
        my_uniques.append(pd.unique(obs_file[each].ravel()))
    big_Dict = dict(zip(wanted_cols, my_uniques))
    return big_Dict


"""
Compare the new file to an old one, looking for any missinfg dimensions/dimension items (depending on findstring)
"""
def dict_compare_missing(old_file, new_file, findstring):

    problems_new = []

    all_keys = old_file.keys()
    for key in all_keys:
        if findstring in key:
            for each in old_file[key]:
                if each not in new_file[key]:
                    problems_new.append(each)    
    return problems_new
    
    
"""
Compare the new file to an old one, looking for any missinfg dimensions/dimension items (depending on findstring)
"""
def dict_compare_unexpected(old_file, new_file, findstring):

    problems_old = []
                
    all_keys = new_file.keys()
    for key in all_keys:
        if findstring in key:
            for each in new_file[key]:
                if each not in old_file[key]:
                    problems_old.append(each)  
    return problems_old 
    

"""
Make the file comparissons and output the results to screen
"""
def compare(check, new_file):
    
    import pickle as pk
    old = pk.load( open("CHECK-" + check + ".chk", "rb" ) )
    
    new = create_unique_dict(new_file)

    # Compare the dimension in the old and new files
    missing_d = dict_compare_missing(old,new, 'dim_id')
    unexpected_d = dict_compare_unexpected(old,new, 'dim_id')
    
    # Compare the dimension items in the old and new files
    missing_i = dict_compare_missing(old,new, 'dim_item')
    unexpected_i = dict_compare_unexpected(old,new, 'dim_item')   
    
    if len(missing_d) > 0 or len(unexpected_d) or len(missing_i) > 0 or len(unexpected_i):
        print ''
        print 'ERROR - Something has changed'
        print '-----------------------------'
        for each in missing_d:
            print 'Expected dimensions missing     : "' + str(each) + '"'
        for each in unexpected_d:
            print 'Unexpected dimensions found     : "' + str(each) + '"'
        for each in missing_i:
            print 'Expected dimension item missing : "' + str(each) + '"'
        for each in unexpected_i:
            print 'Unexpected dimension item found : "' + str(each) + '"'
    else:
        print "Dimension check complete."
        print ''



   