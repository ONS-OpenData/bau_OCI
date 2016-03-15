# -*- coding: utf-8 -*-
"""
Created on Fri Oct 09 17:04:09 2015

@author: Mike
"""

import pandas as pd

# smallchecks is a dictionary of lists, each list containing:
# 1. Title of check 'VALIDATION ... etc"
# 2. Result. Starts at Data error so we know if the function hasn't worked
# 3. An empty list, for storing optional supplementary info (line problem was on, etc)
smallchecks = {
                     'obs_count': ['VALIDATE: Observation count is an integer       : >>>  ', 'DATA ERROR!', []],
             'obs_asterix_check': ['VALIDATE: File footer,  ********* Check         : >>>  ', 'DATA ERROR!', []],
                     'obs_type' : ['VALIDATE: Observations are all numeric          : >>>  ', 'DATA ERROR!', []],
               'time_type_year' : ['VALIDATE: Check year times are correct          : >>>  ', 'DATA ERROR!', []],
              'time_type_month' : ['VALIDATE: Check month times are correct         : >>>  ', 'DATA ERROR!', []],
            'time_type_quarter' : ['VALIDATE: Check quarter times correct           : >>>  ', 'DATA ERROR!', []],
              'matched_columns' : ['VALIDATE: Check that paired columns match       : >>>  ', 'DATA ERROR!', []],
                'no_valid_time' : ['VALIDATE: All time types are valid or blank     : >>>  ', 'DATA ERROR!', []],
              'obs_len_correct' : ['VALIDATE: Obs count correct (numerically)       : >>>  ', 'DATA ERROR!', []],
                'double_blanks' : ['VALIDATE: No rows with blank obs+data markings  : >>>  ', 'DATA ERROR!', []],
       'check_blank_topic_dims' : ['VALIDATE: Any blank topic dimensions            : >>>  ', 'DATA ERROR!', []],
  'check_blank_topic_dim_items' : ['VALIDATE: Any blank topic dimension items       : >>>  ', 'DATA ERROR!', []],
         'valid_column_numbers' : ['VALIDATE: A valid number of columns             : >>>  ', 'DATA ERROR!', []],                              
              }



# Checks that the column of topic columns are cleanly divisible by 8
def Chk_valid_number_of_columns(myframe):
    col_nums = len(list(myframe.columns.values)) - 35
    if col_nums % 8 <> 0:
        smallchecks['valid_column_numbers'][1] = 'FAIL'
        smallchecks['valid_column_numbers'][2].append('Dataset has an invalid number of columns')     
    else:
        smallchecks['valid_column_numbers'][1] = 'Ok'        



# Check that there are no blank entries in the topic dimension
def Chk_blank_topic_dims(myframe):
    smallchecks['check_blank_topic_dims'][1] = 'Ok'    
    myframe.fillna('', inplace = True)
    dim_columns = [x for x in list(myframe.columns.values) if 'dim_id_' in x]
    myframe['empty2'] = ''    
    for each in dim_columns:
        myframe['empty2'][myframe[each] == ''] = 'found'
    count = 0
    for each in myframe['empty2'][:-1].values:
        count = count + 1        
        if each == 'found':
            smallchecks['check_blank_topic_dims'][1] = 'FAIL'
            smallchecks['check_blank_topic_dims'][2].append('Dataset has blank topic Dimenion, row ' + str(count + 1))
    myframe['empty2'] = ''
    
    
    
# Check for blank entries in the topic dimension items    
def Chk_blank_topic_dim_items(myframe):
    smallchecks['check_blank_topic_dim_items'][1] = 'Ok'    
    myframe.fillna('', inplace = True)
    dim_columns = [x for x in list(myframe.columns.values) if 'dim_item_id_' in x]
    myframe['empty2'] = ''    
    for each in dim_columns:
        myframe['empty2'][myframe[each] == ''] = 'found'
    count = 0
    for each in myframe['empty2'][:-1].values:
        count = count + 1        
        if each == 'found':
            smallchecks['check_blank_topic_dim_items'][1] = 'FAIL'
            smallchecks['check_blank_topic_dim_items'][2].append('Dataset has blank topic Dimenion item, row ' + str(count + 1))  
    myframe['empty2'] = ''  
    
    

# Check that there are no rows with a blank entry in both the observation and data markings columns
def Chk_double_blanks(myframe):
    tempframe = myframe[:]
    tempframe.fillna('', inplace = True)
    tempframe['observation'] = tempframe['observation'].astype(str)
    tempframe['data_marking'] = tempframe['data_marking'].astype(str)    
    tempframe['observation'] = tempframe['observation'] + tempframe['data_marking'] 
    count = 0    
    for x in tempframe['observation'].values:
        count = count + 1
        if len(x) < 1:        
            smallchecks['double_blanks'][1] = 'FAIL'
            smallchecks['double_blanks'][2].append('Obs and data markings are both blank, on row ' + str(count))
        else:
            smallchecks['double_blanks'][1] = 'Ok'



# Check that the observation count in the file footer is correct
def Chk_obs_len_correct(myframe):
    if int((len(myframe)-1)) != int(myframe['data_marking'][-1:].values[0]):
        smallchecks['obs_len_correct'][1] = 'FAIL'
        smallchecks['obs_len_correct'][2].append('Obs count in the footer is wrong. Shows ' + str(myframe['data_marking'][-1:].values[0]) + ' expecting ' + str(len(myframe)-1))
    else:
        smallchecks['obs_len_correct'][1] = 'Ok'



# CHECK THAT YEAR TIMES ARE CORRECTLY FORMATTED
def Chk_year_time(myframe):
    timeslice = myframe[myframe['time_type'] == 'Year'][:]
    smallchecks['time_type_year'][1] = 'Ok'
    count = 0          
    for each in timeslice['time_dim_item_id'].values:
        count = count + 1
        try:
            each = int(each)            
            if each > 2025 or each < 1950:
                smallchecks['time_type_year'][1] = 'FAIL'
                smallchecks['time_type_year'][2].append('Year outside bounds (1950 - 2025). "' + str(each) + '" on row ' + str(count + 1))
        except ValueError:
            smallchecks['time_type_year'][1] = 'FAIL'
            smallchecks['time_type_year'][2].append('Not an integer. "' + str(each) + '" on row ' + str(count + 1))



# CHECK THAT MONTH TIMES ARE CORRECTLY FORMATTED
def Chk_month_time(myframe):
    timeslice = myframe[myframe['time_type'] == 'Month'][:]
    smallchecks['time_type_month'][1] = 'Ok' 

    # Check the month Part
    count = 0
    for each in timeslice['time_dim_item_id'].values:
        count = count + 1        
        valid = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']        
        month = each[:3]
        if month not in valid:
            smallchecks['time_type_month'][1] = 'FAIL'
            smallchecks['time_type_month'][2].append('Not a valid month = ' + str(each[:3]) + ' on row ' + str(count + 1))
       
    # check the year part
    count = 0
    for each in timeslice['time_dim_item_id'].values:
        ayear = each[4:]        
        count = count + 1
        try:
            ayear = int(ayear)
            if ayear < 1950 or ayear > 2025:
                smallchecks['time_type_month'][1] = 'FAIL'
                smallchecks['time_type_month'][2].append('Month with invalid year = ' + str(ayear) + ' on row ' + str(count + 1))
        except:
                smallchecks['time_type_month'][1] = 'FAIL'
                smallchecks['time_type_month'][2].append('Month with invalid year = ' + str(ayear) + ' on row ' + str(count + 1))     

    
    for each in timeslice['time_dim_item_id'].values:    
        if len(each) != 8:
                smallchecks['time_type_month'][1] = 'FAIL'
                smallchecks['time_type_month'][2].append('Not the expected eight characters = "' + str(each) + '" on row ' + str(count + 1))           



# CHECK THAT QUARTER TIMES ARE CORRECTLY FORMATTED
def Chk_quarter_time(myframe):
    timeslice = myframe[myframe['time_type'] == 'Quarter'][:]
    smallchecks['time_type_quarter'][1] = 'Ok' 

    # Check the month Part
    count = 0
    for each in timeslice['time_dim_item_id'].values:
        count = count + 1        
        valid = ['Q1', 'Q2', 'Q3', 'Q4']        
        quarter = each[-2:]
        if quarter not in valid:
            smallchecks['time_type_quarter'][1] = 'FAIL'
            smallchecks['time_type_quarter'][2].append('Not a valid quarter = "' + str(each[-2:]) + '" on row ' + str(count + 1))
            
    # check the year part
    count = 0
    for each in timeslice['time_dim_item_id'].values:
        ayear = each[:4]        
        count = count + 1
        try:
            ayear = int(ayear)
            if ayear < 1950 or ayear > 2025:
                smallchecks['time_type_quarter'][1] = 'FAIL'
                smallchecks['time_type_quarter'][2].append('Quarter with invalid year = ' + str(ayear) + ' on row ' + str(count + 1))
        except:
                smallchecks['time_type_quarter'][1] = 'FAIL'
                smallchecks['time_type_quarter'][2].append('Quarter with invalid year = ' + str(ayear) + ' on row ' + str(count + 1))     

    
    for each in timeslice['time_dim_item_id'].values:    
        if len(each) != 7:
                smallchecks['time_type_quarter'][1] = 'FAIL'
                smallchecks['time_type_quarter'][2].append('Not the expected seven characters = "' + str(each) + '" on row ' + str(count + 1))     
            
        
        
# CHECK THAT THERE'S NO FLOATING POINT (.0) ON THE OBSERVATION COUNT        
def Chk_obs_count(myframe):
    myslice = myframe.iloc[-1:len(myframe)][:]
    value = myslice['data_marking'].values
    if '.0' in value:
        smallchecks['obs_count'][1] = 'FAIL'
    else:
        smallchecks['obs_count'][1] = 'Ok'



# CHECK THAT THE OBSERVATION COLUMN FOOTER IS 9*'S AND ONLY APPEARS ONCE
def Chk_asterix_check(myframe):
    myslice = myframe[-1:]
    if myslice['observation'].all() != '*********':
        smallchecks['obs_asterix_check'][1] = 'FAIL'
        smallchecks['obs_asterix_check'][2].append('Failed because >> No valid ********* footer') 
    else:
        smallchecks['obs_asterix_check'][1] = 'Ok'            



# CHECK THAT THERE ARE NO NON-NUMERIC VALUES IN THE OBSERVATION COLUMN
def Chk_obs_type(myframe):
    myslice = myframe['observation'][myframe['observation'] != '*********'][:]    
    smallchecks['obs_type'][1] = 'Ok'
    count = 0
    for each in myslice:
            count = count + 1
            try:
                float(each)
            except ValueError:
                if each != '':
                    smallchecks['obs_type'][1] = 'FAIL'
                    smallchecks['obs_type'][2].append('Problem obs: "' + str(each) + '" on row ' + str(count + 1))               



# CHECK THAT ALL PAIRED COLUMNS ARE SUITABLE DUPLICATES
def Chk_matched_columns(myframe):
    smallchecks['matched_columns'][1] = 'Ok'
    all_headers = list(myframe.columns.values)
    check1 = [x for x in all_headers if 'dim_id_' in x]
    check2 = [x for x in all_headers if 'dimension_label_eng_' in x]
    for x in range(0, len(check1)):
        if myframe[check1[x]].all() != myframe[check2[x]].all():
                smallchecks['matched_columns'][1] = 'FAIL'
                smallchecks['matched_columns'][2].append('Column "' + str(check1[x]) + '" and column "' + str(check2[x]) + '" do not match')  



# CHECK THAT WE HAVE ONLY VALID TIME TYPES
def Chk_valid_time_type(myframe):
    count = 0
    for each in myframe['time_type'].values[:-1]:
        count = count + 1
        if each != 'Year' and each != 'Quarter' and each != 'Month' and each != '':
                smallchecks['no_valid_time'][1] = 'FAIL'
                smallchecks['no_valid_time'][2].append('Not a valid time type: "' + str(each) + '" on row ' + str(count + 1))                  
        else:
                smallchecks['no_valid_time'][1] = 'Ok'               



def small_checks(myframe, filename):

    import timeit
    start_time = timeit.default_timer()
    
    debugging = False
    
    # Load the frame and tun each function in turn)
    Chk_obs_count(myframe)
    if debugging == True:
        print ''
        print 'Chk_obs_count                 ', timeit.default_timer() - start_time
    
    Chk_asterix_check(myframe)
    if debugging == True:
        print 'Chk_asterix_check             ', timeit.default_timer() - start_time
    
    Chk_obs_type(myframe)
    if debugging == True:
        print 'Chk_obs_type                  ', timeit.default_timer() - start_time
    
    Chk_year_time(myframe)
    if debugging == True:
        print 'Chk_year_time                 ', timeit.default_timer() - start_time
    
    Chk_month_time(myframe)
    if debugging == True:
        print 'Chk_month_time                ', timeit.default_timer() - start_time
    
    Chk_quarter_time(myframe)
    if debugging == True:
        print 'Chk_quarter_time              ', timeit.default_timer() - start_time
    
    Chk_matched_columns(myframe)
    if debugging == True:
        print 'Chk_matched_columns           ', timeit.default_timer() - start_time
    
    Chk_valid_time_type(myframe)
    if debugging == True:
        print 'Chk_valid_time_type           ', timeit.default_timer() - start_time
    
    Chk_obs_len_correct(myframe)
    if debugging == True:
        print 'Chk_obs_len_correct           ', timeit.default_timer() - start_time
    
    Chk_double_blanks(myframe)
    if debugging == True:
        print 'Chk_double_blanks             ', timeit.default_timer() - start_time
    
    Chk_valid_number_of_columns(myframe)
    if debugging == True:
        print 'Chk_valid_number_of_columns   ', timeit.default_timer() - start_time
    
    Chk_blank_topic_dims(myframe)
    if debugging == True:
        print 'Chk_blank_topic_dims          ', timeit.default_timer() - start_time
    
    Chk_blank_topic_dim_items(myframe)
    if debugging == True:
        print 'Chk_blank_topic_dim_items     ', timeit.default_timer() - start_time
    
    
    print ''
    print '-------------------------------'
    print 'Validating file: ' + str(filename)
    print '-------------------------------'
    foundfail = False
    for each in smallchecks:
        if debugging == True:
            print smallchecks[each][0] + smallchecks[each][1]
    for each in smallchecks:
                if len(smallchecks[each][2]) > 0:
                    foundfail = True
                    print  smallchecks[each][0] + smallchecks[each][1]
                    print ''
                    print '--- Details ---'
                    outcount = 0
                    for i in smallchecks[each][2]:
                        if outcount < 5:
                            print i
                        outcount = outcount + 1
                    if outcount > 4:
                        print 'Displaying 5 of ' + str(outcount) + ' issues.' 
                    print '------------------------'
                    raw_input('Press any key to continue')
                    print '------------------------'
    if foundfail == False:
        print 'File validation complete.'

def frame_checks(myframe, filename):
    small_checks(myframe, filename)


