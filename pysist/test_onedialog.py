import sys
import tkinter as tk
from onedialog import *
# from tkinter import simpledialog


if __name__ == "__main__":

    def test():
        # master, text='', buttons=[], default=None, 
        # cancel=None, title=None, class_=None
        root = Tk()
        def doit(root=root):
            d = onedialog(root,
                         text="This is a test dialog.  "
                              "Would this have been an actual dialog, "
                              "the buttons below would have been glowing "
                              "in soft pink light.\n"
                              "Do you believe this?",
                         buttons=["Yes", "No", "Cancel"],
                         default=0,
                         cancel=2,
                         title="onedialog")
            
            print(d.go())
            
            logger.info(askstring("String", "Enter a string", 
                            initval='Hollow',
                            minlen=1, 
                            maxlen=10,
                            parent=root))
            print()
            logger.info(askpassword("Password", "Enter your password", 
                            initval='Hollow World',
                            show='*',
                            minlen=8,
                            maxlen=15,
                            mincap=1,
                            minnum=1,
                            logval=False,
                            returnhex=True,
                            parent=root))
            print()
            logger.info(askemailaddress("Email Address", "Enter your email address", 
                            initval='your.name@yahoo.com.au',
                            minlen=8,
                            maxlen=40,
                            illegals=[' ', '='],
                            parent=root))
            print()
            logger.info(askbytes("String to bytes", "Enter a string", 
                            initval='Hollow World',
                            minlen=1,
                            maxlen=15,
                            returnhex=False,
                            parent=root))
            print()
            logger.info(askbytearray("String to bytearray", "Enter a string", 
                            initval='Hollow World',
                            minlen=1,
                            maxlen=15,
                            returnhex=False,
                            parent=root))
            print()
            logger.info(askinteger("Integer", "Enter a Integer", 
                            initval=-45, 
                            minval=-50, 
                            maxval=50,
                            parent=root))
            print()
            logger.info(askfloat("Float", "Enter a float",
                            initval=00041.9785, 
                            minval=0.0, 
                            maxval=50.0,
                            parent=root))
            print()
            logger.info(askbool("Bool", "Enter a bool", 
                            initval='1', 
                            strict=False,
                            parent=root))
            print()
            logger.info(asklist("List", "Enter a list", 
                            initval="['Hollow', 'World']",
                            parent=root))
            print()
            logger.info(asknonetuple("None", "Enter a 'None' value", 
                            initval='null', 
                            strict=False,
                            parent=root))
            print()
            logger.info(askmultitype("Password", "Enter your password", str, 
                            subtype='pw', # force the password sub process
                            show='*', # Show a '*' instead of each input char
                            initval='Hollow World', # initial input string value
                            minlen=8, # Obvious
                            maxlen=15, # Obvious
                            mincap=1,
                            minnum=1,
                            logval=False, # don't show password in the log
                            returnhex=True, # Return input as a hex string
                            illegals=[' ', '='], # illegal password characters
                            parent=root))
            print()
            logger.info(askmultitypetuple("List", "Enter a List", list, 
                            initval="['Hollow', 'World']",
                            parent=root))
            print()
            logger.info(askmultitypetuple("Dictionary", "Enter a dict", dict, 
                            initval="{'Hollow': 'World'}",
                            parent=root))
            print()
            logger.info(askmultitypetuple("Set", "Enter a set", set, 
                            initval="{'Hollow', 'World'}",
                            parent=root))
            # ~ try:
                # ~ print()
                # ~ logger.info(askmultitypetuple("Error", "Forcing Error", frozenset, 
                            # ~ initval="{'Hollow', 'World'}",
                            # ~ parent=root))
            # ~ except (NameError):
                # ~ logger.exception("Illegal type request.")

        t = Button(root, text='Test', command=doit)
        t.pack()
        q = Button(root, text='Quit', command=t.quit)
        q.pack()
        t.mainloop()
    
    test()
