# -*- coding: utf-8 -*-
"""
Created on Tue May 12 10:50:04 2015

@author: Rob
"""

from ONSdatabaker.constants import *

def per_file(tabs):
    return "Table 5"
    
def per_tab(tab):
    
    table_label = tab.excel_ref("C2").parent()
    anchor = tab.excel_ref("A6")
    
    req_rows = anchor.shift(0,3).fill(DOWN)
    req_cols = anchor.shift(RIGHT).fill(RIGHT)
    
    obs = req_rows.waffle(req_cols).is_not_blank()
    #obs = tab.excel_ref('C27').expand(DOWN).expand(RIGHT)    
    
    type_head = req_rows - req_rows.same_row(obs)
    type_head = type_head | anchor
    type_head.dimension("Type", CLOSEST, ABOVE)
    anchor.fill(DOWN).dimension("Type 2", DIRECTLY, LEFT)
    
    anchor.fill(RIGHT).is_not_blank().dimension("Year", CLOSEST, LEFT)
    anchor.shift(DOWN).fill(RIGHT).is_not_blank().dimension("Time Other" , CLOSEST, LEFT)
    
    yield obs