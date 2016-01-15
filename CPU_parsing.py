
import numpy as np 
import matplotlib.pyplot as plt
from dateutil.parser import *
from datetime import *
from matplotlib.legend import Legend
import tkinter as tk
from tkinter import filedialog
from matplotlib.widgets import CheckButtons


#Declaration of variables
CPU_amended = []

#def functions
def func(label):
    if label == 'usr':
        l1.set_visible(not l1.get_visible())
    elif label == 'sys':
        l2.set_visible(not l2.get_visible())
    elif label == 'nic':
        l3.set_visible(not l3.get_visible())
    elif label == 'idle':
     	l4.set_visible(not l4.get_visible())
    elif label == 'io':
        l5.set_visible(not l5.get_visible())
    elif label == 'irq':
     	l6.set_visible(not l6.get_visible())
    elif label == 'sirq':
        l7.set_visible(not l7.get_visible())
    plt.draw()




#Ask for CPU_usage file in text format
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

CPU_usage = open(file_path,'r')
CPU = CPU_usage.readlines()

#modification of loaded 2D list and transposing to prepare for numpy manipulation
for i,c in enumerate(CPU):
	c = c.split(';')
	CPU_amended.append(c)
	
CPU_amended.pop(0)
CPU_np = np.array(CPU_amended)
CPU_np = np.transpose(CPU_amended)
dates = [parse(s) for s in CPU_np[0]]
		
		
#Plots using matplotlib
fig, ax = plt.subplots()

l1, = ax.plot(dates, CPU_np[1],'k-', label='usr')
l2, = ax.plot(dates, CPU_np[3],'b-', label='sys')
l3, = ax.plot(dates, CPU_np[5],'r-', label='nic')
l4, = ax.plot(dates, CPU_np[7],'c-', label='idle')
l5, = ax.plot(dates, CPU_np[9],'m-', label='io')
l6, = ax.plot(dates, CPU_np[11],'y-', label='irq')
l7, = ax.plot(dates, CPU_np[13],'k-', label='sirq')
plt.subplots_adjust(left=0.2)
#legend = ax.legend(loc='upper right', shadow=True)
ax.legend(loc='upper right')
plt.xticks(rotation=25)
ax.set_title('CPU monitoring')


#rax = plt.axes([0.05, 0.4, 0.1, 0.15])
#check = CheckButtons(rax,('usr','sys','nic','idle','io','irq','sirq'),(True,True,True,True,True,True,True))    
#check.on_clicked(func)


plt.show()


