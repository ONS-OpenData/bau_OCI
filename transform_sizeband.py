# -*- coding: utf-8 -*-
"""
Created on Fri Oct 09 08:38:43 2015

@author: Mike
"""

import pandas as pd
import sys
import transform_lib as tf
import compare as cp

pd.options.mode.chained_assignment = None  # default='warn'

load_file = sys.argv[1]
obs_file = pd.read_csv(load_file)

# Get rid of footer
obs_file = obs_file[obs_file['observation'] != '*********']

# tidy dimensions 1. Get rod of rogue mid-cell value whistespace
obs_file['dim_item_id_1'] = obs_file['dim_item_id_1'].astype(str)
obs_file['dim_item_id_1'] = obs_file['dim_item_id_1'].map(lambda x: x.strip())
obs_file['dim_item_id_1'] = obs_file['dim_item_id_1'].map(lambda x: ' '.join(x.split()))
obs_file['dimension_item_label_eng_1'] = obs_file['dim_item_id_1']
obs_file.fillna('', inplace = True)

# Round observations to a whole number
obs_file['observation'] = obs_file['observation'].astype(float)
obs_file['observation'] = obs_file['observation'].map(lambda x: round(x, 0))
obs_file['observation'] = obs_file['observation'].astype(str)
obs_file['observation'] = obs_file['observation'].map(lambda x: x.replace('.0', ''))

# Make other dimensions string
obs_file['dim_item_id_2'] = obs_file['dim_item_id_2'].astype(str)
obs_file['dim_item_id_3'] = obs_file['dim_item_id_3'].astype(str)
obs_file['dim_item_id_4'] = obs_file['dim_item_id_4'].astype(str)
obs_file['dim_item_id_5'] = obs_file['dim_item_id_5'].astype(str)

# Remove any duplication in 2, 3, 4 and 
obs_file['dim_item_id_4'][obs_file['dim_item_id_4'] == obs_file['dim_item_id_3']] = ''
obs_file['dimension_item_label_eng_4'] = obs_file['dim_item_id_4']

obs_file['dim_item_id_3'][obs_file['dim_item_id_2'] == obs_file['dim_item_id_3']] = ''
obs_file['dimension_item_label_eng_3'] = obs_file['dim_item_id_3']

# Now concatenate 2, 3, 4, 5
obs_file['dim_item_id_2'] = obs_file['dim_item_id_2'].map(str.strip) + " " \
                                         + obs_file['dim_item_id_3'].map(str.strip) + " " \
                                         + obs_file['dim_item_id_4'].map(str.strip) + " " \
                                         + obs_file['dim_item_id_5'].map(str.strip)                                         
obs_file['dimension_item_label_eng_2'] = obs_file['dim_item_id_2']

# -- Sort out the infrastructure/infr-structure/infranstr-ucture thing --
# This is our best solution to this recurring data inconsistency problem
"""
THE FOLLOWING ARE ALL VARIATIONS OF INFRASTRCUTURE, ADD MORE AS NEEDED, SAME FORMAT
"""
bad_list = ['Infrastruc - ture', 'Infra - structure', 'Infrast - ructure', 'Infrastr - ucture',
            'Infrastruc- ture', 'Infra- structure', 'Infrast- ructure', 'Infrastr- ucture',
            'Infrastruc -ture', 'Infra -structure', 'Infrast -ructure', 'Infrastr -ucture',
            'Infrastruc-ture', 'Infra-structure', 'Infrast-ructure', 'Infrastr-ucture',
            'Infras-tructure', 'Infras-tructure'
]
for each in bad_list:
    obs_file['dim_item_id_2'] = obs_file['dim_item_id_2'].map(lambda x: x.replace(each, 'Infrastructure'))
obs_file['dimension_item_label_eng_2'] = obs_file['dim_item_id_2']

obs_file = tf.dismiss(obs_file, ['dim_id_3', 'dim_id_4', 'dim_id_5'])

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
