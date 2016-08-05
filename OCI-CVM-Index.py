# -*- coding: utf-8 -*-
"""
Created on Tue May 12 10:50:04 2015

@author: Rob
"""

from ONSdatabaker.constants import *

def per_file(tabs):
    return ["Table 1a", "Table 1b"]
    
def per_tab(tab):
    
    table_label = tab.excel_ref("C2").parent()
    
    if not table_label.filter(contains_string("NON-SEASONAL")):
        tab.dimension("SA / SNA", "Non-seasonally adjusted")
    else:
        tab.dimension("SA / SNA", "Seasonally adjusted")
    
    anchor = tab.filter(contains_string ("Period")).assert_one()
    
    req_rows = anchor.shift(0,2).fill(DOWN)
    req_cols = anchor.shift(RIGHT).fill(RIGHT)
    
    obs = req_rows.waffle(req_cols).is_not_blank()
    obs = obs - tab.excel_ref('A10').expand(RIGHT)
    
    anchor.shift(UP).fill(RIGHT).parent().is_not_blank().dimension("Construction Sectors", CLOSEST, LEFT)
    anchor.fill(RIGHT).parent().is_not_blank().dimension("Sector 2", CLOSEST, LEFT)
    anchor.shift(DOWN).fill(RIGHT).dimension("Sector 3", DIRECTLY, ABOVE)
    anchor.shift(0,2).fill(RIGHT).dimension("Sector 4", DIRECTLY, ABOVE)
    
    req_rows.is_not_blank().dimension("Year" , CLOSEST, ABOVE)
    req_rows.shift(RIGHT).dimension("Time Other" , DIRECTLY, LEFT)
    
    yield obs