# -*- coding: utf-8 -*-
"""
Created on Tue May 12 10:50:04 2015

@aut00hor: Rob
"""

from ONSdatabaker.constants import *

def per_file(tabs):
    return ["Table 2a", "Table 2b", "Table 4", "Table 4a"]
    
def per_tab(tab):
    
    table_label = tab.excel_ref("C3").parent()
    
    if table_label.filter(contains_string("NON-SEASONAL")):
        tab.dimension("SA / SNA", "Non-seasonally adjusted")
    else:
        tab.dimension("SA / SNA", "Seasonally adjusted")
    
    if table_label.filter(contains_string("VALUE")):
        tab.dimension("Value / Volume", "Value, current prices")
    else:
        tab.dimension("Value / Volume", "Volume")
    
    
    anchor = tab.excel_ref('A7')
    
    req_rows = anchor.shift(0,2).fill(DOWN)
    req_cols = anchor.shift(RIGHT).fill(RIGHT)
    
    obs = req_rows.waffle(req_cols).is_not_blank()
    obs = obs - tab.excel_ref('A10').expand(RIGHT)
    
    anchor.shift(UP).fill(RIGHT).parent().is_not_blank().dimension("Construction Sectors", CLOSEST, LEFT)
    anchor.fill(RIGHT).parent().is_not_blank().dimension("Sector 2", CLOSEST, LEFT)
    anchor.shift(DOWN).fill(RIGHT).dimension("Sector 3", CLOSEST, LEFT)
    anchor.shift(0,2).fill(RIGHT).dimension("Sector 4", CLOSEST, LEFT)
    
    req_rows.is_not_blank().dimension("Year" , CLOSEST, ABOVE)
    req_rows.shift(RIGHT).dimension("Time Other" , DIRECTLY, LEFT)
    
    yield obs