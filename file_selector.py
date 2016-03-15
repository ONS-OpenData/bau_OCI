# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 17:48:22 2015

@author: Mike
"""

import tkFileDialog
import Tkinter as tk


def get_file1():
    global file1 
    path = tkFileDialog.askopenfilename(filetypes=[("Excel Spreadsheet","*.xls")])
    file1.set(path)    
        
def run():
    runfiles(file1.get())

def runfiles(source):
    
    import shutil
    import os    

    # Get the directory of the selected file
    # Compare length with both \ and / to cover possible other os use
    filepath = source[: source.rfind('\\')]
    if len(source[: source.rfind('/')]) < len(filepath):
        filepath = source[: source.rfind('/')]
    filepath = filepath.replace('/', '\\')    # Swap / for \ so we can compare the two

    # Compare the current working directory with the above.
    # If its the same, we dont want to move or split anything - the files already in the working directory!
    if filepath != os.getcwd():    
        shutil.move(source, os.getcwd())    
    
    # now get the name out of it    

    filename = source.split('/')
    filename = filename[len(filename)-1]
    filename = '"' + filename + '"'

    """
    Now the flename is sorted. This part is just bulding a list of commands, then executing them
    """
    linestolaunch = []
    
    linestolaunch.append('bake --preview OCI-CVM-Index.py ' + filename)
    linestolaunch.append('bake --preview OCI-CVM-Growth.py ' + filename)
    linestolaunch.append('bake --preview OCI-CVM-Prices.py ' + filename)
    linestolaunch.append('bake --preview OCI-CVM-Indicator.py ' + filename)
    linestolaunch.append('bake --preview OCI-CVM-Sizeband.py ' + filename)
    linestolaunch.append('bake --preview OCI-CVM-Type.py ' + filename)
    linestolaunch.append('bake --preview OCI-CVM-Region.py ' + filename)
    
    # Take the quotes back off
    filename = filename[1:-1]  
    
    #Get rid of file extension
    filename = filename[:-4]
    
    linestolaunch.append('python transform_growth_index.py "data-' + filename + '-OCI-CVM-Growth-.csv" Growth')
    linestolaunch.append('python transform_growth_index.py "data-' + filename + '-OCI-CVM-Index-.csv" Index')
    linestolaunch.append('python transform_indicator.py "data-' + filename + '-OCI-CVM-Indicator-.csv" Indicator')
    linestolaunch.append('python transform_prices.py "data-' + filename + '-OCI-CVM-Prices-.csv" Prices')
    linestolaunch.append('python transform_region.py "data-' + filename + '-OCI-CVM-Region-.csv" Region')
    linestolaunch.append('python transform_sizeband.py "data-' + filename + '-OCI-CVM-Sizeband-.csv" Sizeband')
    linestolaunch.append('python transform_type.py "data-' + filename + '-OCI-CVM-Type-.csv" Type')     
    
    import subprocess as sp     
    for each in linestolaunch:
                p = sp.Popen(each, shell=True) #, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                p.communicate()

    print 'Processing Complete. Close either this window or the GUI to exit'
    
    
    
    
"""
THE FOLLOWING CODE IS JUST FOR THE GUI
"""
            
root = tk.Tk()
file1 = tk.StringVar()

description = 'TRANSFORM TOOL - Output in the Construction Industry, V1.0'
label = tk.Label(root, text=description)
label.pack()

description = 'INFO - 1 Excel input. 7 CSV Datasets outputs. Databaker may complain about date formatting, this is expected.'
label = tk.Label(root, text=description)
label.pack()

tk.Button(text='Select Source File', command=get_file1).pack()
tk.Label(root, textvariable=file1).pack()

tk.Button(text='Databake, Transform & Validates Files', command=run).pack()
# tk.Button(text='Compare', command=convert).pack()
root.mainloop()



