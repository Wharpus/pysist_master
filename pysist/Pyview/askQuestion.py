#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  askQuestion.py
#  
#  2020 Wharpusware <wharpus@gmail.com>
#

# illustration of icon - Info 
import tkinter as tk #python3

from tkinter import messagebox

main = tk.Tk() 

def check(): 
    result = tk.messagebox.askquestion("Form", 
                        "Do you wish to continue?", 
                        icon ='info') 
    print(result)
    if result == 'yes':
        # They either clicked the default 'Yes' button or hit return key
        pass # Do something
    else:
        # They either clicked 'No' or closed the dialog window
        pass # Do something or nothing

main.geometry("100x100") 
B1 = tk.Button(main, text = "check", command = check) 
B1.pack() 

main.mainloop() 
