import sys
import numpy as np 
import matplotlib.pyplot as plt
from dateutil.parser import *
from datetime import *
from matplotlib.legend import Legend
import tkinter as tk
from tkinter import filedialog
from matplotlib.widgets import CheckButtons
import os
import tarfile


def main():
    #Ask for CPU_usage file in text format
    root = tk.Tk()
    root.withdraw()
    Files_sel = filedialog.askopenfilenames()

    Files_l = list(Files_sel)
    Files_l.sort()
       
    file_name = input("Enter a file name:")
        
    for files in Files_l:
    
        tar = tarfile.open(files, mode='r')
        f = tar.getnames()
        
        for filename in f:
            if 'meminfo' in filename:

                f=tar.extractfile(filename)
                content=f.read().splitlines()
                
                header = header_create(content)
                
                mem_parse(content, header,file_name)



def header_create(content):
    header  = []
    headers = []
    for i,c in enumerate(content):
        header.append(c.split()[0])
    for item in header:
        b = str(item)[2:]
        b = b[:-2]
        headers.append(b)
    headers.append('Cal. free memory')
    
    return(headers)
    
def mem_parse(content,header,file_name):
    
    mem_info = []
    mem_info_num = []
    header_final = []
    count = 0

    for i,c in enumerate(content):

        mem_info.append(c.split()[1])
    
    for item in mem_info:
        b = str(item)[2:]
        b = b[:-1]
        mem_info_num.append(b)
                
    mem_info_num.append(str(int(mem_info_num[1])+int(mem_info_num[2])+ int(mem_info_num[3])-int(mem_info_num[19])))            
                
    
    with open(file_name,'a') as f:
        if os.stat(file_name).st_size == 0:
           f.writelines(';'.join(str(list) for list in header))
           f.write('\n')
        f.writelines(';'.join(str(list) for list in mem_info_num))
        f.write('\n')
    

        
if __name__ == "__main__": 
    main() 










