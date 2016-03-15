# -*- coding: utf-8 -*-
"""
Created on Fri Oct 09 08:38:43 2015

@author: Mike
"""

import pandas as pd
import sys
import transform_lib as tf
import compare as cp

load_file = sys.argv[1]
obs_file = pd.read_csv(load_file)

pd.options.mode.chained_assignment = None  # default='warn'

# Get rid of footer
obs_file = obs_file[obs_file['observation'] != '*********']

# Make other dimensions string
obs_file.fillna('', inplace = True)
obs_file['dim_item_id_1'] = obs_file['dim_item_id_1'].astype(str)
obs_file['dim_item_id_2'] = obs_file['dim_item_id_2'].astype(str)
obs_file['dim_item_id_3'] = obs_file['dim_item_id_3'].astype(str)
obs_file['dim_item_id_4'] = obs_file['dim_item_id_4'].astype(str)

# Remove any duplication in 2, 3, 4 and 5
obs_file['dim_item_id_4'][obs_file['dim_item_id_4'] == obs_file['dim_item_id_3']] = ''
obs_file['dimension_item_label_eng_4'] = obs_file['dim_item_id_4']

obs_file['dim_item_id_3'][obs_file['dim_item_id_3'] == obs_file['dim_item_id_2']] = ''
obs_file['dimension_item_label_eng_3'] = obs_file['dim_item_id_3']

obs_file['dim_item_id_2'][obs_file['dim_item_id_1'] == obs_file['dim_item_id_2']] = ''
obs_file['dimension_item_label_eng_2'] = obs_file['dim_item_id_2']

# Now concatenate 2, 3, 4, 5
obs_file['dim_item_id_1'] = obs_file['dim_item_id_1'].map(str.strip) + " " \
                                         + obs_file['dim_item_id_2'].map(str.strip) + " " \
                                         + obs_file['dim_item_id_3'].map(str.strip) + " " \
                                         + obs_file['dim_item_id_4'].map(str.strip)
obs_file['dimension_item_label_eng_1'] = obs_file['dim_item_id_1']

# -- Sort out the infrastructure/infr-structure/infranstr-ucture thing --
# This is our best solution to this recurring data inconsistency problem
"""
THE FOLLOWING ARE ALL VARIATIONS OF INFRASTRCUTURE, ADD MORE AS NEEDED, SAME FORMAT
"""
bad_list = ['Infrastruc - ture', 'Infra - structure', 'Infrast - ructure', 'Infrastr - ucture',
            'Infrastruc- ture', 'Infra- structure', 'Infrast- ructure', 'Infrastr- ucture',
            'Infrastruc -ture', 'Infra -structure', 'Infrast -ructure', 'Infrastr -ucture',
            'Infrastruc-ture', 'Infra-structure', 'Infrast-ructure', 'Infrastr-ucture',
]
for each in bad_list:
    obs_file['dim_item_id_1'] = obs_file['dim_item_id_1'].map(lambda x: x.replace(each, 'Infrastructure'))
obs_file['dimension_item_label_eng_1'] = obs_file['dim_item_id_1']


# SORTING OUT TIME
obs_file.fillna('', inplace = True)
obs_file['dim_item_id_6'] = obs_file['dim_item_id_6'].astype(str)
obs_file['dim_item_id_6'] = obs_file['dim_item_id_6'].str[0:3]
# 1.Assume everything is month
obs_file['time_type'] = obs_file['time_type'].astype(str)
obs_file['time_type'] = 'Month'
# 2. Get length of time 2. Anything thanks 0 is a year
obs_file['dim_item_id_6'] = obs_file['dim_item_id_6'].map(str.strip)
obs_file['temp_dim'] = obs_file['dim_item_id_6'].map(lambda x: len(x))
obs_file['time_type'][obs_file['temp_dim'] == 0] = 'Year'
# 2.) Set quarters if the lngth is 2
obs_file['time_type'][obs_file['temp_dim'] == 2] = 'Quarter'

# Populate time based on the timetype
obs_file['dim_item_id_5'] = obs_file['dim_item_id_5'].astype(str)
obs_file['dim_item_id_5'] = obs_file['dim_item_id_5'].map(lambda x: x.replace('.0', ''))
obs_file['time_dim_item_id'][obs_file['time_type'] == 'Month'] = obs_file['dim_item_id_6'] + ' ' + obs_file['dim_item_id_5']
obs_file['time_dim_item_id'][obs_file['time_type'] == 'Quarter'] = obs_file['dim_item_id_5'] + ' ' + obs_file['dim_item_id_6']
obs_file['time_dim_item_id'][obs_file['time_type'] == 'Year'] = obs_file['dim_item_id_5']
obs_file['time_dim_item_label_eng'] = obs_file['time_dim_item_id']
obs_file = tf.dismiss(obs_file, ['dim_id_2', 'dim_id_3', 'dim_id_4', 'dim_id_5', 'dim_id_6'])
obs_file = obs_file.drop('temp_dim', axis=1) 

# Add file footer
count = len(obs_file)
obs_file = obs_file.set_value(len(obs_file), 'observation', '*********')
obs_file = obs_file.set_value(len(obs_file) -1, 'data_marking', str(count))

import validation_tool as vt
out_filename = 'transform'+load_file[4:]
vt.frame_checks(obs_file, out_filename)

obs_file.to_csv(out_filename, index=False)

# Now run the coparissons against past datasets
cp.compare(sys.argv[2], out_filename)   
                                

