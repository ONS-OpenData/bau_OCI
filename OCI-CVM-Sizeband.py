# -*- coding: utf-8 -*-
"""
Created on Tue May 12 10:50:04 2015

@aut00hor: Rob
"""

from ONSdatabaker.constants import *

def per_file(tabs):
    return "Table 10"
    
def per_tab(tab):
    
    table_label = tab.excel_ref("C2").parent()
    
    anchor = tab.filter(contains_string ("Period")).assert_one()
    
    req_rows = anchor.fill(DOWN)
    req_cols = anchor.shift(2,0).fill(RIGHT)
    
    obs = req_rows.waffle(req_cols).is_not_blank()

    anchor.fill(DOWN).shift(1,-1).parent().dimension("Employment Size Band" , DIRECTLY, LEFT)
    
    anchor.shift(0,-3).fill(RIGHT).parent().is_not_blank().dimension("Construction Sectors", CLOSEST, LEFT)
    anchor.shift(0,-2).fill(RIGHT).parent().is_not_blank().dimension("Sector 2", CLOSEST, LEFT)
    anchor.shift(UP).fill(RIGHT).dimension("Sector 3", CLOSEST, LEFT)
    anchor.fill(RIGHT).dimension("Sector 4", CLOSEST, LEFT)
    
    req_rows.is_not_blank().dimension(TIME, CLOSEST, ABOVE)
    
    obs = obs - tab.filter(contains_string ('Further information on the IDBR')).expand(RIGHT)
    
    yield obs