# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 12:36:30 2015

@author: Mike

Compares the dimensions and dimension items within a CSV and a Check_file (.chk - a python dictionary in a file that retains the same info)

"""

import pandas as pd
import sys
import numpy as np


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
    import os
    old = pk.load( open(os.getcwd() + '/Check Files/' + "CHECK-" + check + ".chk", "rb" ) )
    
    new = create_unique_dict(new_file)

    # Compare the dimension in the old and new files
    missing_d = dict_compare_missing(old,new, 'dim_id')
    unexpected_d = dict_compare_unexpected(old,new, 'dim_id')
    
    # Compare the dimension items in the old and new files
    missing_i = dict_compare_missing(old,new, 'dim_item')
    unexpected_i = dict_compare_unexpected(old,new, 'dim_item')   
    
    if len(missing_d) > 0 or len(unexpected_d) or len(missing_i) > 0 or len(unexpected_i):
        print ''
        print '-----------------------------'
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
        print '------------------------'
        raw_input('Press any key to continue')
        print '------------------------'
    else:
        print "Dimension check complete."
        print ''



   
