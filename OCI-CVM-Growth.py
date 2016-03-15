# -*- coding: utf-8 -*-
"""
Created on Tue May 12 10:50:04 2015

@author: Rob
"""

from databaker.constants import *

def per_file(tabs):
    return ["Table 3a", "Table 3b"]
    
def per_tab(tab):
    
    table_label = tab.excel_ref("C2").parent()
    anchor = tab.filter(contains_string ("Period")).assert_one()
    
    req_rows = anchor.shift(0,2).fill(DOWN)
    req_cols = anchor.shift(RIGHT).fill(RIGHT)
    
    obs = req_rows.waffle(req_cols).is_not_blank()
    obs = obs - tab.excel_ref('A10').expand(RIGHT)
    
    table_label.dimension("Growth", CLOSEST, ABOVE)
    anchor.shift(UP).fill(RIGHT).parent().is_not_blank().dimension("Construction Sectors", CLOSEST, LEFT)
    anchor.fill(RIGHT).parent().is_not_blank().dimension("Sector 2", CLOSEST, LEFT)
    anchor.shift(DOWN).fill(RIGHT).dimension("Sector 3", DIRECTLY, ABOVE)
    anchor.shift(0,2).fill(RIGHT).dimension("Sector 4", DIRECTLY, ABOVE)
    
    req_rows.is_not_blank().dimension("Year" , CLOSEST, ABOVE)
    req_rows.shift(RIGHT).dimension("Time Other" , DIRECTLY, LEFT)
    
    yield obs