#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  askQuestion.py
#  
#  2020 Wharpusware <wharpus@gmail.com>
#

# A sample of all messagebox dialogs
import tkinter as tk #python3
from tkinter import messagebox 

root = tk.Tk() 
root.geometry("300x200") 

w = tk.Label(root, text ='GeeksForGeeks', font = "50") 
w.pack() 

result = tk.messagebox.showinfo("showinfo", "Information") 
print(result) # returns 'ok'
if result == 'ok':
    # They clicked the default 'OK' button or closed the dialog window
    print('Yay')
    pass # Do something

result = tk.messagebox.showwarning("showwarning", "Warning") 
print(result) # returns 'ok'
if result == 'ok':
    # They clicked the default 'OK' button or closed the dialog window
    print('Yay')
    pass # Do something

result = tk.messagebox.showerror("showerror", "Error") 
print(result) # returns 'ok'
if result == 'ok':
    # They clicked the default 'OK' button or closed the dialog window
    print('Yay')
    pass # Do something

result = tk.messagebox.askquestion("askquestion", "Are you sure?") 
print(result) # returns 'yes' or 'no'
if result == 'yes':
    # They either clicked the default 'Yes' button or hit return key
    print('Yay')
    pass # Do something
else:
    # They either clicked 'No' or closed the dialog window
    print('Damn')
    pass # Do something or nothing

result = tk.messagebox.askokcancel("askokcancel", "Want to continue?") 
print(result) # returns True or False
if result: 
    # They either clicked the default 'Ok' button or hit return key
    print('Yay')
    pass # Do something
else:
    # They either clicked 'Cancel' or closed the dialog window
    print('Damn')
    pass # Do something or nothing

result = tk.messagebox.askyesno("askyesno", "Find the value?") 
print(result) # returns True or False
if result:
    # They either clicked the default 'Yes' button or hit return key
    print('Yay')
    pass # Do something
else:
    # They either clicked 'No' or closed the dialog window
    print('Damn')
    pass # Do something or nothing

result = tk.messagebox.askretrycancel("askretrycancel", "Try again?") 
print(result) # returns True or False
if result:
    # They either clicked the default 'Retry' button or hit return key
    print('Yay')
    pass # Do something
else:
    # They either clicked 'Cancel' or closed the dialog window
    print('Damn')
    pass # Do something or nothing

root.mainloop() 
