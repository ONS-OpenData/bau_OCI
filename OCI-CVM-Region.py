# -*- coding: utf-8 -*-
"""
Created on Tue May 12 10:50:04 2015

@author: Rob
"""

from ONSdatabaker.constants import *

def per_file(tabs):
    return "Table 6"
    
def per_tab(tab):
    
    table_label = tab.excel_ref("C2").parent
    #anchor = tab.filter(contains_string ("PERIOD")).assert_one()
    anchor = tab.excel_ref('A6')    
    
    req_rows = tab.excel_ref('A10').expand(DOWN)
    # req_cols = anchor.shift(RIGHT).fill(RIGHT)
    
    #obs = req_rows.waffle(req_cols).is_not_blank()
    #obs = obs - tab.excel_ref('A10').expand(RIGHT)
    
    obs = tab.excel_ref('B11').fill(RIGHT).expand(DOWN).is_not_blank()
    
    tab.excel_ref('B6').fill(RIGHT).parent().is_not_blank().filter(is_not(contains_string("illion"))).dimension("Area", CLOSEST, LEFT)
    tab.excel_ref('B7').fill(RIGHT).parent().is_not_blank().dimension("Construction Sectors", CLOSEST, LEFT)
    tab.excel_ref('B8').fill(RIGHT).parent().is_not_blank().dimension("Sector 2", CLOSEST, LEFT)
    tab.excel_ref('B9').fill(RIGHT).parent().is_not_blank().dimension("Sector 4", DIRECTLY, ABOVE)
    
    req_rows.is_not_blank().dimension("Year" , CLOSEST, ABOVE)
    req_rows.shift(RIGHT).dimension("Time Other" , DIRECTLY, LEFT)
    
    obs = obs - tab.excel_ref('A11').expand(RIGHT)
    
    yield obs