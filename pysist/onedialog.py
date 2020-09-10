#
# pysist.onedialog uses modified code from _QueryDialog
#
# Copyright (c) 2020 by 'The Flying Wharpus' at Wharpus Ware <wharpus@gmail.com>
#
# This copyright applies to: 
#    onedialog._QueryDialog,
#    onedialog.multitypeddialog
# 
# Original Dialog, askinteger, askfloat, askstring code copyright by:
# fredrik@pythonware.com
# http://www.pythonware.com
#
"""pysist.onedialog enforces a multitude of different input types.

Onedialog contains the following public objects:
The onedialog is a drop-in replacement for tkinter.simpledialog

_QueryString and_QueryDialog contains the all of the functionality 
behind each multitypedialog call.

multitypedialog -- is the object called by all of the lesser dialogs 
and can be called directly if you wish to make your own custom dialog.

askpassword -- get a length limited enforced string from the user.
The password input value by default is not shown in the logs.
It checks input for illegal characters or strings, which can be 
overridden by supplying your own list of characters or strings.
It can also return the input converted to a hexadecimal string.
    RETURNS: A string object, or None.

askemailaddress -- get a length limited enforced string from the user.
The input value can also be forced to not log the input value.
It checks input for illegal characters and strings using a regex, 
which can also be overridden by supplying your own re.match raw string.
It can also return the input converted to a hexadecimal string.
    RETURNS: A string object, or None.

askstring -- get a input string from the user.
It can enforce a length limited input.
It can check for input for illegal characters and strings.
It can also return the input converted to a hexadecimal string.
    RETURNS: A string object, or None.

askinteger -- enforce a integer within a range from the user.
    RETURNS: A integer object, or None.

askfloat -- enforce a float within a range from the user.
    RETURNS: A float object, or None.

askbool -- enforce a bool (either strict or rational) from the user.
Defaults to strict. To allow rational bool input, supply a strict=False
    RETURNS: A bool object (True of False), or None.

asklist -- get a valid list input from the user.
It can enforce min and max items within the list.
It can enforce the types of items allowed within the list by supplying 
a list of allowed types. ie allow=[str, int, float, bool]
    RETURNS: A list object, or None.

asktuple -- enforce a tuple within a range from the user.
It can enforce min and max items within the list.
It can enforce the types of items allowed within the list by supplying 
a list of allowed types. ie allow=[str, int, float, bool]
    RETURNS: A tuple object, or None.

askset -- enforce a set within a range from the user.
It can enforce min and max items within the list.
It can enforce the types of items allowed within the list by supplying 
a list of allowed types. ie allow=[str, int, float, bool]
    RETURNS: A set object, or None.

askdict -- enforce a dict within a range from the user.
It can enforce min and max items within the list.
It can enforce the types of items allowed within the list by supplying 
a list of allowed types. ie allow=[str, int, float, bool]
    RETURNS: A dict object, or None.

askbytes -- get input from the user and return a bytes object.
It can enforce a length limited input.
It can check for input for illegal characters and strings.
It can also return the input converted to a hexadecimal string.
    RETURNS: A bytes object, or None.

askbytearray -- get input from the user and return a bytearray object.
It can enforce a length limited input.
It can check for input for illegal characters and strings.
It can also return the input converted to a hexadecimal string.
    RETURNS: A bytearray object, or None.

asknonetuple -- enforce a None value within a range from the user.
    RETURNS a 3 part tuple in the format: 
    (True, convertedInput, convertedType) if all went well
    (False, unconvertedInput, unconvertedType) if could not convert
    (None, unconvertedInput, unconvertedType, errorString) if an error occurred

askmultitype -- get a variety of supported valid python types.
    RETURNS: An object of requested type, or None.

askmultitypetuple -- get a variety of supported valid python types.
    RETURNS a 3 or 4 part tuple in the format: 
    (True, convertedInput, convertedType) if all went well
    (False, unconvertedInput, unconvertedType) if could not convert
    (None, unconvertedInput, unconvertedType, errorString) if an error occurred
"""
import os
from tkinter import *
from tkinter import messagebox
import tkinter # used in _QueryDialog for tkinter._default_root
from ast import literal_eval
import logging
import re

# The onedialog logging function
def init_logging(level='warning'):

    Logger = logging.getLogger(__name__)
    level = level.lower()
    if level == 'debug':
        Logger.setLevel(logging.DEBUG)
    elif level == 'info':
        Logger.setLevel(logging.INFO)
    elif level == 'warning':
        Logger.setLevel(logging.WARNING)
    elif level == 'error':
        Logger.setLevel(logging.ERROR)
    elif level == 'critical':
        Logger.setLevel(logging.CRITICAL)
    else:
        Logger.setLevel(logging.WARNING)
    
    LOG_DIR = os.path.join(os.getcwd(), "logs", "")
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    # File Logger
    fileHandler = logging.FileHandler("{}{}.log".format(LOG_DIR, __name__))
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    fileHandler.setFormatter(formatter)
    Logger.addHandler(fileHandler)
    
    # Console Logger
    consoleHandler = logging.StreamHandler()
    cformatter = logging.Formatter('%(levelname)s : %(message)s')
    consoleHandler.setFormatter(cformatter)
    Logger.addHandler(consoleHandler)

    return Logger

# Get the logger:
# valid levels: 'debug', 'info', 'warning', 'error', 'critical'
# default level: 'warning'
logger = init_logging('debug')
# start logging:
logger.warning("Welcome to the 'onedialog' log")



class onedialog:

    def __init__(self, master,
                 text='', buttons=[], default=None, cancel=None, 
                 title=None, class_=None):
        logger.debug('{}: {}({})'.format(self.__class__.__name__, 
                                sys._getframe().f_code.co_name, 
                                "'{}', '{}', {}, {}, {}, {}, {}, {}"
                                .format(self, master, text, buttons, 
                                    default, cancel, title, class_)))
        if class_:
            self.root = Toplevel(master, class_=class_)
        else:
            self.root = Toplevel(master)
        if title:
            self.root.title(title)
            self.root.iconname(title)
        self.message = Message(self.root, text=text, aspect=400)
        self.message.pack(expand=1, fill=BOTH)
        self.frame = Frame(self.root)
        self.frame.pack()
        self.num = default
        self.cancel = cancel
        self.default = default
        self.root.bind('<Return>', self.return_event)
        for num in range(len(buttons)):
            s = buttons[num]
            b = Button(self.frame, text=s,
                       command=(lambda self=self, num=num: self.done(num)))
            if num == default:
                b.config(relief=RIDGE, borderwidth=8)
            b.pack(side=LEFT, fill=BOTH, expand=1)
        self.root.protocol('WM_DELETE_WINDOW', self.wm_delete_window)
        self._set_transient(master)

    def _set_transient(self, master, relx=0.5, rely=0.3):
        widget = self.root
        widget.withdraw() # Remain invisible while we figure out the geometry
        widget.transient(master)
        widget.update_idletasks() # Actualize geometry information
        if master.winfo_ismapped():
            m_width = master.winfo_width()
            m_height = master.winfo_height()
            m_x = master.winfo_rootx()
            m_y = master.winfo_rooty()
        else:
            m_width = master.winfo_screenwidth()
            m_height = master.winfo_screenheight()
            m_x = m_y = 0
        w_width = widget.winfo_reqwidth()
        w_height = widget.winfo_reqheight()
        x = m_x + (m_width - w_width) * relx
        y = m_y + (m_height - w_height) * rely
        if x+w_width > master.winfo_screenwidth():
            x = master.winfo_screenwidth() - w_width
        elif x < 0:
            x = 0
        if y+w_height > master.winfo_screenheight():
            y = master.winfo_screenheight() - w_height
        elif y < 0:
            y = 0
        widget.geometry("+%d+%d" % (x, y))
        widget.deiconify() # Become visible at the desired location

    def go(self):
        self.root.wait_visibility()
        self.root.grab_set()
        self.root.mainloop()
        self.root.destroy()
        return self.num

    def return_event(self, event):
        if self.default is None:
            self.root.bell()
        else:
            self.done(self.default)

    def wm_delete_window(self):
        if self.cancel is None:
            self.root.bell()
        else:
            self.done(self.cancel)

    def done(self, num):
        self.num = num
        self.root.quit()


"""This class builds the dialog windows"""
class Dialog(Toplevel):

    '''Class to open dialogs.

    This class is intended as a base class for custom dialogs
    '''

    def __init__(self, parent, title=None):
        logger.debug('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "'{}', {}".format(parent, title)))
        '''Initialize a dialog.

        Arguments:

            parent -- a parent window (the application window)

            title -- the dialog title
        '''
        Toplevel.__init__(self, parent)

        self.withdraw() # remain invisible for now
        # If the master is not viewable, don't
        # make the child transient, or else it
        # would be opened withdrawn
        if parent.winfo_viewable():
            self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        if self.parent is not None:
            self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                      parent.winfo_rooty()+50))

        self.deiconify() # become visible now

        self.initial_focus.focus_set()

        # wait for window to appear on screen before calling grab_set
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def destroy(self):
        '''Destroy the window'''
        self.initial_focus = None
        Toplevel.destroy(self)

    # construction hooks

    def body(self, master):
        '''create dialog body.

        return widget that should have initial focus.
        This method should be overridden, and is called
        by the __init__ method.
        '''
        pass

    def buttonbox(self):
        '''add standard button box.

        override if you do not want the standard buttons
        '''

        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        try:
            self.apply()
        finally:
            self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        if self.parent is not None:
            self.parent.focus_set()
        self.destroy()

    # command hooks

    def validate(self):
        '''validate the data

        This method is called automatically to validate the data before the
        dialog is destroyed. By default, it always validates OK.
        '''

        return 1 # override

    def apply(self):
        '''process the data

        This method is called automatically to process the data, *after*
        the dialog is destroyed. By default, it does nothing.
        '''

        pass # override

# |-----------------------|
# | convenience dialogues |
# |-----------------------|

"""This class does all the enforcing of your dialog rules"""
class _QueryDialog(Dialog):

    def __init__(self, title, prompt, reqType,
                subtype = None,
                initial = None,
                minval = None,
                maxval = None,
                maxlen = None,
                minlen = None,
                minitems = None,
                maxitems = None,
                mincap = None,
                minlow = None,
                minnum = None,
                minsym = None,
                strict = True,
                logval = True,
                gethex = False,
                illegals = None,     # ['=', 'eval', 'exec', '__'],
                allowed = None,
                regex = None,        # r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                walk = False,  # walk contents checking fields
                types = None,
                parent = None):

        logger.debug('{}: {}({})'
            .format(self.__class__.__name__, sys._getframe().f_code.co_name, 
            "'{}', {}, {}, '{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}"
                .format(title, prompt, reqType, initial, minval, maxval, maxlen, 
                        minlen, mincap, minnum, minsym, subtype, strict, logval, gethex, 
                        illegals, regex, walk, parent)))
        if not parent:
            parent = tkinter._default_root

        if reqType == None:
            self.reqType = type(reqType)
        else:
            self.reqType = reqType
        
        if subtype is not None:
            self.subtype = subtype = subtype.lower()
            if self.subtype not in ['pw', 'email']:
                logger.error("Unsupported subtype requested. Subtype '%s' is unsupported.", 
                            self.subtype)
                messagebox.showwarning(
                    "Unsupported subtype request",
                    "Subtype '{}' is unsupported.. "
                    "Supported subtypes are 'pw' and 'email'. "
                    "Returning None.".format(str(self.subtype)),
                    parent = self
                )
                logger.error("Reverting to normal string input.")
                subtype = None
        
        self.prompt = prompt
        self.minval = minval
        self.maxval = maxval
        self.maxlen = maxlen
        self.minlen = minlen
        self.maxitems = maxitems
        self.minitems = minitems
        self.mincap = mincap
        self.minlow = minlow
        self.minnum = minnum
        self.minsym = minsym
        self.strict = strict
        self.subtype = subtype
        self.logval = logval
        self.gethex = gethex
        self.illegals = illegals
        self.allowed = allowed
        self.regex = regex
        self.walk = walk
        self.types = types
        
        self.initial = initial
        
        Dialog.__init__(self, parent, title)

    def destroy(self):
        self.entry = None
        Dialog.destroy(self)

    def body(self, master):

        w = Label(master, text=self.prompt, justify=LEFT)
        w.grid(row=0, padx=5, sticky=W)

        self.entry = Entry(master, name="entry")
        self.entry.grid(row=1, padx=5, sticky=W+E)

        if self.initial is not None:
            self.entry.insert(0, str(self.initial))
            self.entry.select_range(0, END)

        return self.entry

    def validate(self):
        try:
            result = self.entry.get()
            if self.logval == True:
                logger.debug("Raw input string: '%s'.", result)
            else:
                logger.debug("Raw input string: '********'.")
        except (ValueError, SyntaxError, TypeError, OverflowError, AssertionError):
            logger.exception("Illegal Value... Please try again")
            messagebox.showwarning(
                "Illegal value",
                "Illegal Value... Please try again",
                parent = self
            )
            return 0
        
        if self.reqType not in [str, int, float, bool, list, tuple, set, dict, bytes, bytearray, type(None)]:
            logger.error("Unsupported request. Request for %s is unsupported.", 
                        self.reqType)
            messagebox.showwarning(
                "Unsupported request",
                "Request for {} is unsupported.. "
                "Request a type you can convert. "
                "Returning the value as a string.".format(str(self.reqType)),
                parent = self
            )
            logger.info("Returning the original input string.")
            return self._validate_str(result)
        
        # Check for subtypes before its parent type
        if self.subtype == 'pw':
            return self._validate_pw(result)
            
        if self.subtype == 'email':
            return self._validate_email(result)
        
        if self.reqType == str:
            return self._validate_str(result)
            
        if self.reqType == int:
            return self._validate_int(result)
            
        if self.reqType == float:
            return self._validate_float(result)
            
        if self.reqType == bool:
            return self._validate_bool(result)
            
        if self.reqType == list:
            return self._validate_list(result)
            
        if self.reqType == tuple:
            return self._validate_tuple(result)
            
        if self.reqType == set:
            return self._validate_set(result)
            
        if self.reqType == dict:
            return self._validate_dict(result)
        
        if self.reqType == bytes:
            return self._validate_bytes(result)

        if self.reqType == bytearray:
            return self._validate_bytearray(result)

        if self.reqType == type(None):
            return self._validate_none(result)
        
        self.result = result
        return 1


    # Functions used by validation Functions to check input
    def _check_len(self, testobj):
        logger.debug("Doing _check_len().")
        
        if self.minlen is not None and len(testobj) < int(self.minlen):
            logger.debug("Minumum length of ({}) not reached.", self.minlen)
            messagebox.showwarning(
                "Min length error",
                "Minumum length of ({}) not reached.\nPlease try again."
                    .format(str(self.minlen)),
                parent = self
            )
            return False
        
        if self.maxlen is not None and len(testobj) > int(self.maxlen):
            logger.debug("Exceeded max length of (%s) chars.", self.maxlen)
            messagebox.showwarning(
                "Max length error",
                "Exceeded max length of({}) chars.\nPlease try again."
                    .format(str(self.maxlen)),
                parent = self
            )
            return False
        logger.debug("_check_len() passed.")
        return True

    def _check_val(self, testobj):
        logger.debug("Doing _check_val().")
        
        if self.minval is not None and self.maxval is not None:
            if testobj < self.reqType(self.minval) or testobj > self.reqType(self.maxval):
                logger.debug("Enter Value between %s and %s... Please try again.", 
                            self.minval, self.maxval)
                messagebox.showwarning(
                    "Value out of range",
                    "Enter Value between {} and {}.\nPlease try again."
                        .format(self.minval, self.maxval),
                    parent = self
                )
                return False
        
        if self.minval is not None and testobj < self.reqType(self.minval):
            logger.debug("The minimum value is (%s)... Please try again.", 
                        self.minval)
            messagebox.showwarning(
                "Value too small",
                "The minimum value is ({})...\nPlease try again."
                    .format(str(self.minval)),
                parent = self
            )
            return False

        if self.maxval is not None and testobj > self.reqType(self.maxval):
            logger.debug("The maximum value is (%s)... Please try again.", 
                        self.maxval)
            messagebox.showwarning(
                "Value too large",
                "The allowed maximum value is ({})...\nPlease try again."
                    .format(str(self.maxval)),
                parent = self
            )
            return False

        logger.debug("_check_val() passed.")
        return True

    def _check_items(self, testobj):
        
        if self.minitems is None and self.maxitems is None:
            return True
            
        logger.debug("Doing _check_items().")
        
        if type(testobj) not in ['list', 'tuple', 'dict', 'set']:
            logger.debug("testobj type %s is not supported.", type(testobj))
            return True
        
        if self.minitems is not None and len(testobj) < int(self.minitems):
            logger.debug("Minimum number items of (%s) not reached.", self.minitems)
            messagebox.showwarning(
                "Min items error",
                "Minimum number items of ({}) not reached.\nPlease try again."
                    .format(str(self.minitems)),
                parent = self
            )
            return False
                
        if self.maxitems is not None and len(testobj) > int(self.maxitems):
            logger.debug("Exceeded max number of (%s) items.", self.maxitems)
            messagebox.showwarning(
                "Max items error",
                "Exceeded max number of ({}) item.\nPlease try again."
                    .format(str(self.maxitems)),
                parent = self
            )
            return False
        logger.debug("_check_items() passed.")
        return True

    def _check_equals(self, testobj):
        logger.debug("Doing _check_equals().")
        
        illegal = False
        illegalcnt = 0
        
        if not self.logval:
            logger.debug("testobj: '********'")
        else:
            logger.debug("testobj: '%s'", testobj)
            
        if '=' in testobj:
            logger.debug("Found a '=', so having a closer look...")
            indexlist = [m.start() for m in re.finditer('=', testobj)]
            if not self.logval:
                logger.debug("index of '=': {}: '********'.")
            else:
                logger.debug("index of '=': {}: \"{}\".".format(str(indexlist), testobj))
            # ie [0, 5, 6, 15] or -1
            if indexlist != -1:
                for x in range(len(indexlist)):
                    index = indexlist[x]
                    logger.debug('index: %s', index)
                    if index+1 not in indexlist and index-1 not in indexlist:
                        logger.debug("There is no '=' either side, so check more...")
                        if index != 0 and testobj[index-1] not in ['=', '!', '<', '>']:
                            logger.debug("There is no '=', '!', '<', or '>' before it, so is BAD.")
                            # it's an illegal one
                            illegal = True
                            illegalcnt += 1
                            logger.debug("Assignment operator found at position %s character %s.", index, index+1)
                        elif index == 0:
                            illegal = True
                            illegalcnt += 1
                            logger.debug("Assignment operator found at position %s character %s.", index, index+1)
                        else:
                            logger.debug("It has a '=', '!', '<', or '>' before it, so is OK.")
                            
                    # It's a comparison and is safe
        if illegal:
            logger.debug("Found %s assignment operators.", illegalcnt)
            messagebox.showwarning(
                "Illegal assignment error",
                "Found ({}) illegal assignment operators.\nPlease try again."
                    .format(str(illegalcnt)),
                parent = self
            )
            return False
        logger.debug("_check_equals() passed.")
        return True

    def _check_illegals(self, testobj):
        
        if self.illegals is None:
            return True
        
        logger.debug("Doing _check_illegals().")
        
        illegal = False
        illegalcnt = 0
        #checklist = ['ast.', 'eval(', 'exec(', '__', 
        #             'sys.exit(', 'os.', '.destroy(']
        
        checklist = self.illegals
        for check in checklist:
            if check in testobj:
                illegal = True
                illegalcnt += 1
                logger.debug("Found illegal content '%s' found in string.", check)

        if illegal:
            logger.debug("Found %s illegal items.", illegalcnt)
            messagebox.showwarning(
                "Illegal Character error",
                "Found ({}) illegal chars.\nPlease try again."
                    .format(str(illegalcnt)),
                parent = self
            )
            return False
        
        logger.debug("_check_illegals() passed.")
        return True

    def _check_regex(self, testobj, re_name='entry'):
        
        if self.regex is None:
            return True
        
        logger.debug("Doing _check_regex().")

        if self.regex:
            restr = self.regex
        else:
            restr = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"
        
        if not re.match(restr, testobj):
            logger.debug("'%s' is not a valid %s. Using regex: r%r ", testobj, re_name, restr)
            messagebox.showwarning(
                "Invalid Email",
                "Regex says: '{}' is not a valid {}.\nPlease try again."
                    .format(testobj, re_name),
                parent = self
            )
            return False
        logger.debug("_check_regex() passed.")
        return True

    # Validation helper functions
    def _postvalidate(self, result): # returns converted and tested result or original result
        if self.reqType not in [dict, list, tuple, set]:
            self.result = result
            return 1
        resultType = type(result)
        logger.debug("Doing _postvalidate(%s) for type %s.", result, resultType)
        
        if resultType != self.reqType:
            # Try getting the literal evaluation to get the real type of inputStr
            try:
                convertedInput = literal_eval(result)
            except (ValueError, SyntaxError, TypeError, OverflowError, AssertionError) as err:
                if logval == True:
                    e = "Postvalidate error converting '{}' to type {}".format(result, inputType)
                else:
                    e = "Postvalidate error converting '********' to type {}".format(inputType)
                logger.exception(e)
                messagebox.showwarning(
                    "Error: invalid input",
                    "Error: invalid input.\nPlease try again.",
                    parent = self
                )
                return 0
        
        if not self._check_items(convertedInput): # returns false on fail
            return 0
        
        convertedType = type(convertedInput)
        logger.debug("Finished _postvalidate(%s) is now type %s.", convertedInput, convertedType)
        self.result = convertedInput
        return 1


    def _validate_str(self, result):

        if not self._check_len(result): # check against minlen and maxlen
            return 0
        if not self._check_equals(result): # check for assignment operator
            return 0
        if not self._check_illegals(result): # check against illegals list
            return 0
        if not self._check_regex(result): # check against regex match
            return 0
                
        if self.gethex == True:
            # string with encoding 'utf-8'
            result = bytearray(result, 'utf-8').hex()

        self.result = result
        return 1

    def _validate_pw(self, result):

        if not self._check_len(result): # returns false on fail
            return 0

        if not self._check_equals(result): # returns false on fail
            return 0

        if not self._check_illegals(result): # returns false on fail
            return 0

        # check lowercase count
        if self.minlow is not None and int(self.minlow) > 0:
            strlen = len(result)
            lowcount = 0
            for i in range(strlen):
                if result[i].islower():
                    lowcount += 1
            if lowcount < int(self.mincap):
                logger.debug("Minumum of (%s) lowercase not reached.", self.mincap)
                messagebox.showwarning(
                    "Min lowercase error",
                    "Minumum of ({}) lowercase not reached.\nPlease try again."
                        .format(str(self.mincap)),
                    parent = self
                )
                return 0
        # check uppercase count
        if self.mincap is not None and int(self.mincap) > 0:
            strlen = len(result)
            capcount = 0
            for i in range(strlen):
                if result[i].isupper():
                    capcount += 1
            if capcount < int(self.mincap):
                logger.debug("Minumum of (%s) capitals not reached.", self.mincap)
                messagebox.showwarning(
                    "Min capitals error",
                    "Minumum of ({}) capitals not reached.\nPlease try again."
                        .format(str(self.mincap)),
                    parent = self
                )
                return 0
        # check number count
        if self.minnum is not None and int(self.minnum) > 0:
            strlen = len(result)
            numcount = 0
            for i in range(strlen):
                if result[i].isdigit():
                    numcount += 1
            if numcount < int(self.minnum):
                logger.debug("Minumum of (%s) numbers not reached.", self.minnum)
                messagebox.showwarning(
                    "Min numbers error",
                    "Minumum of ({}) numbers not reached.\nPlease try again."
                        .format(str(self.minnum)),
                    parent = self
                )
                return 0
        # check symbol count
        if self.minsym is not None and int(self.minsym) > 0:
            strlen = len(result)
            symcount = 0
            for i in range(strlen):
                if result[i].isalpha():
                    continue
                elif result[i].isdigit():
                    continue
                else:
                    symcount += 1
                
            if symcount < int(self.minsym):
                logger.debug("Minumum of (%s) symbols not reached.", self.minsym)
                messagebox.showwarning(
                    "Min symbols error",
                    "Minumum of ({}) symbols not reached.\nPlease try again."
                        .format(str(self.minsym)),
                    parent = self
                )
                return 0

        # ~ if not self._check_regex(result, 'password'): # returns false on fail
            # ~ return 0

        # return hex if asked
        
        if self.gethex == True:
            # string with encoding 'utf-8'
            result = bytearray(result, 'utf-8').hex()

        self.result = result
        return 1

    def _validate_email(self, result):

        if not self._check_len(result): # returns false on fail
            return 0
                    
        if not self._check_regex(result, 'email address'): # check against regex match
            return 0
        
        self.result = result
        return 1

    def _validate_int(self, result):
        result = result.lstrip().rstrip().lstrip('0')
        if result == '':
            result = '0'

        if not self._check_len(result): # check against minlen and maxlen
            return 0
        if not self._check_equals(result): # check for assignment operator
            return 0
        if not self._check_illegals(result): # check against illegals list
            return 0
        if not self._check_regex(result, 'integer'): # check against regex match
            return 0
        
        try:
            testresult = int(result)
        except (ValueError, SyntaxError, TypeError, OverflowError, AssertionError):
            logger.exception("Only integers are excepted... Please try again.")
            messagebox.showwarning(
                "Integer required",
                "Only integers are excepted...\nPlease try again",
                parent = self
            )
            return 0

        if not self._check_val(testresult): # returns false on fail
            return 0
        
        self.result = testresult
        return 1

    def _validate_float(self, result):
        if result[0] == '.':
            result = '0' + result
        
        if not self._check_len(result): # check against minlen and maxlen
            return 0
        if not self._check_equals(result): # check for assignment operator
            return 0
        if not self._check_illegals(result): # check against illegals list
            return 0
        
        try:
            testresult = float(result)
        except (ValueError, SyntaxError, TypeError, OverflowError, AssertionError):
            logger.exception("Only decimals are excepted... Please try again")
            messagebox.showwarning(
                "Decimal required",
                "Only decimals are excepted...\nPlease try again",
                parent = self
            )
            return 0
        
        if not self._check_val(testresult): # returns false on fail
            return 0
        
        self.result = testresult
        return 1

    def _validate_bool(self, result):
        result = result.lstrip().rstrip()
        result = result.lower().capitalize()

        if not self._check_len(result): # check against minlen and maxlen
            return 0
        if not self._check_equals(result): # check for assignment operator
            return 0
        if not self._check_illegals(result): # check against illegals list
            return 0
        
        if self.strict:
            if result not in ['True', 'False']:
                logger.debug("Strict boolean. Enter 'True' or 'False'... Please try again.")
                messagebox.showwarning(
                    "Strictly boolean only",
                    "Enter 'True' or 'False'.\nPlease try again.",
                    parent = self
                )
                return 0
        
        # Not Strict
        elif result not in ['True', 'False', 'Yes', 'No', 'Y', 'N', '0', '1']:
            logger.debug("Implied Boolean allowed. Enter 'True', 'False', 'Yes', 'No', 'Y', 'N', '0', or '1'... Please try again.")
            messagebox.showwarning(
                "Implied Boolean allowed",
                "Enter 'True', 'False', 'Yes', 'No', 'Y', 'N', '0', or '1'.\
                    Please try again.",
                parent = self
            )
            return 0

        # Allow various entries implying true and false
        impliedresult = result
        if impliedresult in ['True', 'Yes', 'Y', '1']:
            result = True
            logger.info("Assigned '{}' as: {}".format(str(impliedresult), str(result)))
        elif impliedresult in ['False', 'No', 'Y', '0']:
            result = False
            logger.info("Assigned '{}' as: {}".format(str(impliedresult), str(result)))
    
        self.result = result
        return 1

    def _validate_list(self, result):

        if not self._check_len(result): # check against minlen and maxlen
            return 0
        if not self._check_equals(result): # check for assignment operator
            return 0
        if not self._check_illegals(result): # check against illegals list
            return 0
        
        # passed all string tests passed
        # so now do any postvalidate tests
        return self._postvalidate(result) # sets self.result and returns 0 or 1

    def _validate_tuple(self, result):

        if not self._check_len(result): # check against minlen and maxlen
            return 0
        if not self._check_equals(result): # check for assignment operator
            return 0
        if not self._check_illegals(result): # check against illegals list
            return 0
        
        # passed all string tests passed
        # so now do any postvalidate tests
        return self._postvalidate(result) # returns 0 or 1

    def _validate_set(self, result):

        if not self._check_len(result): # check against minlen and maxlen
            return 0
        if not self._check_equals(result): # check for assignment operator
            return 0
        if not self._check_illegals(result): # check against illegals list
            return 0
        
        # passed all string tests passed
        # so now do any postvalidate tests
        return self._postvalidate(result) # returns 0 or 1

    def _validate_dict(self, result):

        if not self._check_len(result): # check against minlen and maxlen
            return 0
        if not self._check_equals(result): # check for assignment operator
            return 0
        if not self._check_illegals(result): # check against illegals list
            return 0
        
        # passed all string tests passed
        # do _postvalidate()
        return self._postvalidate(result) # returns 0 or 1

    def _validate_bytes(self, result):

        if not self._check_len(result): # check against minlen and maxlen
            return 0
        if not self._check_equals(result): # check for assignment operator
            return 0
        if not self._check_illegals(result): # check against illegals list
            return 0
        
        result = bytes(result, 'utf-8')
        
        self.result = result
        return 1

    def _validate_bytearray(self, result):

        if not self._check_len(result): # check against minlen and maxlen
            return 0
        if not self._check_equals(result): # check for assignment operator
            return 0
        if not self._check_illegals(result): # check against illegals list
            return 0
        
        result = bytearray(result, 'utf-8')
        
        self.result = result
        return 1

    def _validate_none(self, result):
        result = result.lstrip().rstrip()
        result = result.lower().capitalize()
        
        if not self._check_len(result): # check against minlen and maxlen
            return 0
        if not self._check_equals(result): # check for assignment operator
            return 0
        if not self._check_illegals(result): # check against illegals list
            return 0
        
        if self.strict:
            if result != 'None':
                logger.debug("Strictly 'None' value only... Please try again.")
                messagebox.showwarning(
                    "Strictly 'None' value only",
                    "Enter 'None'.\nPlease try again.",
                    parent = self
                )
                return 0
        
        # Not Strict
        elif result not in ['None', 'Null', 'Nil', '']:
            logger.debug("Implied bool allowed. Enter 'None', 'Null', 'Nil', or leave blank... Please try again.")
            messagebox.showwarning(
                "Implied bool values allowed",
                "Enter 'None', 'Null', 'Nil', or leave blank.\nPlease try again.",
                parent = self
            )
            return 0

        # Allow various entries implying true and false
        impliedresult = result
        if impliedresult in ['None', 'Null', 'Nil', '']:
            result = 'None'
            logger.info("Assigned '{}' as: {}".format(str(impliedresult), result))
    
        self.result = result
        return 1


"""Enforces the show='*' for password input."""
class _QueryString(_QueryDialog):
    def __init__(self, *args, **kw):
        logger.debug('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "args: {}, kw: {}".format(args, kw)))
        if "show" in kw:
            self.__show = kw["show"]
            del kw["show"]
        else:
            self.__show = None
        _QueryDialog.__init__(self, *args, **kw)

    def body(self, master):
        entry = _QueryDialog.body(self, master)
        if self.__show is not None:
            entry.configure(show=self.__show)
        return entry

    def getresult(self):
        return self.entry.get()


"""This is the main function that gets called by the ask* dialogs"""
def multitypedialog(title, prompt, reqType, **kw):
    '''multitypedialog is the "swiss army knife" of input dialogs. 
    It shows a dialog window to get a specified input type from the user, 
    then it tries to return the user input in the requested type.
    If input can't be converted to the required type, it returns the original input string.
    Note: When requesting a str type, the string is returned unprocessed.
    
    You can use just one dialog window to request 10 different python types, including: 
    str, int, float, bool, list, tuple, set, dict, bytes, and None.
    
    ARGUMENTS:
    
        title   - Is the dialog windows title as string, ie 'Enter a string.'
        prompt  - Is the request label text as string, ie 'Please enter your full name.'
        reqtype - str, int, float, bool, list, tuple, set, dict, bytes, bytearray, and None
        
        **kw    - optional allowed kw arguments are:
                  initial  str or None  # Initial value of input field (for all types).
        NEW  -->  subtype  'pw', 'email' or None  # enforce the subtype processing.
        NEW  -->  show     '*' or None  # Show a '*' instead of each input char.
        NEW  -->  minval   int or None  # Minimum value of input field (for numeric requests).
        NEW  -->  maxval   int or None  # Maximum value of input field (for numeric requests).
        NEW  -->  maxlen   int or None  # Maximum length (count of chars or collection items).
        NEW  -->  minlen   int or None  # Maximum length (count of chars or collection items).
        NEW  -->  mincap   int or None  # Minimum number of capital letters required (in passwords).
        NEW  -->  minlow   int or None  # Minimum number of lowercase letters required (in passwords).
        NEW  -->  minnum   int or None  # Minimum number of numbers required (in passwords).
        NEW  -->  minsym   int or None  # Minimum number of symbols required (in passwords). 
                                          Use illegals to specify and bad password chars.
        NEW  -->  illegals list or None # List, tuple, or string containing all illegal chars.
        NEW  -->  regex    raw or None  # A raw (r'') regex string to validate the input with.
        NEW  -->  logval   bool or None # don't show value in the onedialog log. ie passwords.
        NEW  -->  gethex   bool or None # Return input string as a hex string.
        NEW  -->  strict   bool or None # Defaults True, enforce strict True or False inputs.
                  (for bool)              If strict is False, also allow the conversion of 
                                          Yes, No, Y, N, 0, and 1 into True or False values.
        NEW  -->  strict   bool or None # Defaults True, enforce strict 'None' inputs.
                  (for None)              If False, also allow the conversion of 
                                          'null', 'nil' and '' into a None object.
                  parent   root or None # The tkinter root window class link the dialog to, 
                                          and return to after the dialog closes.
    RETURNS: hopefully what you ask for
    
    The multitypedialog returns a 3 item tuple in the format: 
        (True False or None, returnedObject, objectType).
    Item one is True if the returned input IS the type requested.
    Item one is False if the returned input IS NOT the type requested.
    Item one is None if an error occured while processing the input. 
    NOTE: If item one is None, the error string is added to the tuple as the 4th item

    I created this multi-input-type dialog based upon simpledialog._QueryDialog()
    and simpledialog._QueryString() which I have call onedialog.multitypedialog
    '''
    # 'logval' default is True unless otherwise supplied
    if 'logval' not in kw.keys(): 
        kw['logval'] = True
        logval = True
    else:
        logval = kw['logval']

    logger.info('{}: {}({})'.format(onedialog.__class__.__name__, 
                        sys._getframe().f_code.co_name, 
                        "'{}', '{}', {}".format(title, prompt, reqType)))
    # Initialize _QueryString() and get input
    d = _QueryString(title, prompt, reqType, **kw)
    inputStr = d.result
    
    inputType = type(inputStr)
    if logval == True:
        logger.info("Input: '{}' type: {}".format(inputStr, inputType))
    else:
        logger.debug("Input: '********' type: {}".format(inputType))
    if inputStr == 'None':
        inputStr = None
        inputType = type(inputStr)
        if logval == True:
            logger.info("Output: {} type: {}".format(inputStr, inputType))
        else:
            logger.debug("Output: '********' type: {}".format(inputType))
        return (True, inputStr, inputType)

    # print("reqType: {}, inputType: {}".format(reqType, inputType))
    
    # Don't evaluate the string as it is already the reqested type
    if reqType == inputType: # Return it as a 3 part tuple
        if logval == True:
            logger.info("Input is request type, returning. Output: {} type: {}"
                .format(inputStr, inputType))
        else:
            logger.debug("Input is request type, returning. Output: '********' type: {}"
                .format(inputType))
        return (True, inputStr, inputType)
    
    # Input needs evaluating
    if logval == True:
        logger.info("Input reached literal eval. Output: {} type: {}"
            .format(inputStr, inputType))
    else:
        logger.debug("Input reached literal eval. Output: '********' type: {}"
            .format(inputType))
    
    # Try getting the literal evaluation to get the real type of inputStr
    try:
        convertedInput = literal_eval(inputStr)
    except (ValueError, SyntaxError, TypeError, OverflowError, AssertionError) as err:
        if logval == True:
            e = "Error while converting '{}' to type {}".format(inputStr, inputType)
        else:
            e = "Error while converting '********' to type {}".format(inputType)
        logger.exception(e)
        return (None, inputStr, inputType, err) # Can use info for logging entries

    convertedType = type(convertedInput)
    if convertedType is reqType:
        if logval == True:
            logger.info("Output: {} type: {}".format(convertedInput, convertedType))
        else:
            logger.debug("Output: '********' type: {}".format(inputType))
        return (True, convertedInput, convertedType)
        
    if logval == True:
        logger.info("Original output: '{}' type: {}".format(inputStr, inputType))
    else:
        logger.debug("Original output: '********' type: {}".format(inputType))
    return (False, inputStr, inputType)

def askstring(title, prompt, **kw):
    '''get a string from the user
    Drop in replacement for simpledialog.askstring()

    ARGUMENTS:

        title  - Is the dialog windows title as string, ie 'String Input Required.'
        prompt - Is the request label text as string, ie 'Please enter your full name.'
        **kw   - Optional allowed kw arguments are:
                 initial   None or str   Initial value of input field.
        NEW -->  maxlen    None or int   Max input length allowed (in chars).
        NEW -->  minlen    None or int   Min input length required (in chars).
        NEW -->  gethex    Nono or bool  Return input string as a hexidecimal string.
        NEW -->  illegals  None or list  List of illegal characters.
        NEW -->  regex     None or raw   A raw (r'') regex string to validate the input with.

                 parent    None or root  The tkinter root window class to open the dialog from, 
                                         and return to after the dialog closes.
    RETURNS: a string or None
    '''
    result = multitypedialog(title, prompt, str, **kw)    
    if result[0]:
        return result[1]
    else:
        return None

def askpassword(title, prompt, **kw):
    '''get a password from the user

    ARGUMENTS:

        title  - Is the dialog windows title as string, ie 'String Input Required.'
        prompt - Is the request label text as string, ie 'Please enter your full name.'
        **kw   - Optional allowed kw arguments are:
                 initial  None or str    Initial value of input field.
        NEW -->  maxlen   None or int    Maximum input length allowed.
        NEW -->  minlen   None or int    Minimum input length required.
        NEW -->  mincap   None or int    Minimum number of A-Z letters required.
        NEW -->  minnum   None or int    Minimum number of 0-9 digits required.
        NEW -->  minsym   None or int    Minimum number of Non alpha-numeric chars.
        NEW -->  logval   bool or None   Don't show value in the log file. For passwords.
        NEW -->  gethex   bool or None   Return input string as a hex string.
        NEW -->  illegals list or None   List, tuple, or string containing all illegal chars.
        NEW -->  regex    raw or None    A raw (r'') regex string to validate the input with.
        NEW -->  logval   bool or None   Don't show value in the onedialog log. ie passwords.
        NEW -->  gethex   bool or None   Return input string as a hex string.

                 parent   None or root   The tkinter root window class to open the dialog from, 
                                         and return to after the dialog closes.
    RETURNS: a string or None
    '''
    
    if 'subtype' not in kw.keys():
        kw['subtype'] = 'pw'
    if 'show' not in kw.keys():
        kw['show'] = '*'
    if 'logval' not in kw.keys(): 
        kw['logval'] = False
    # ~ if 'illegals' not in kw.keys():
        # ~ kw['illegals'] = [' ', '=']
        
    result = multitypedialog(title, prompt, str, **kw)
    if result[0]:
        return result[1]
    else:
        return None

def askemailaddress(title, prompt, **kw):
    '''get an email address from the user

    ARGUMENTS:

        title  -- Is the dialog windows title as string, ie 'String Input Required.'
        prompt -- Is the request label text as string, ie 'Please enter your full name.'
        **kw   -- Optional allowed kw arguments are:
                  initial  =  None or str   Initial value of input field
        NEW  -->  maxlen   =  None or int   Maximum input length allowed
        NEW  -->  minlen   =  None or int   Minimum input length required
        NEW  -->  mincap   =  None or int   Minimum number of A-Z letters required
        NEW  -->  minnum   =  None or int   Minimum number of 0-9 digits required
        NEW  -->  illegals =  None or list  List of illegal characters

                   parent  = None       The tkinter root window class to open the dialog from, 
                                        and return to after the dialog closes.
    RETURNS: a email address string or None
    '''
    if 'subtype' not in kw.keys():
        kw['subtype'] = 'email'
    # ~ if 'illegals' not in kw.keys():
        # ~ kw['illegals'] = [' ', '=']
        
    result = multitypedialog(title, prompt, str, **kw)
    if result[0]:
        return result[1]
    else:
        return None

def askinteger(title, prompt, **kw):
    '''get an integer value from the user
    Drop in replacement for simpledialog.askinteger()

    ARGUMENTS:

        title  -- Is the dialog windows title as string, ie 'String Input Required.'
        prompt -- Is the request label text as string, ie 'Please enter your full name.'
        **kw   -- Optional allowed kw arguments are:
                  initial =  None or str  Initial value of input field
        NEW  -->  minval  =  None or int  Minimum value of input field
        NEW  -->  maxval  =  None or int  Maximum value of input field

                   parent  = None       The tkinter root window class to open the dialog from, 
                                        and return to after the dialog closes.
    RETURNS: a integer value or None
    '''
    result = multitypedialog(title, prompt, int, **kw)
    if result[0]:
        return result[1]
    else:
        return None

def askfloat(title, prompt, **kw):
    '''get a float from the user
    Drop in replacement for simpledialog.askfloat()

    ARGUMENTS:

        title  -- Is the dialog windows title as string, ie 'String Input Required.'
        prompt -- Is the request label text as string, ie 'Please enter your full name.'
        **kw   -- Optional allowed kw arguments are:
                  initial =  None or str  Initial value of input field
        NEW  -->  minval  =  None or int  Minimum value of input field
        NEW  -->  maxval  =  None or int  Maximum value of input field

                   parent  = None       The tkinter root window class to open the dialog from, 
                                        and return to after the dialog closes.
    RETURNS: a float or None
    '''
    result = multitypedialog(title, prompt, float, **kw)
    if result[0]:
        return result[1]
    else:
        return None

def askbool(title, prompt, **kw):
    '''get a boolean value from the user

    ARGUMENTS:

        title  -- Is the dialog windows title as string, ie 'String Input Required.'
        prompt -- Is the request label text as string, ie 'Please enter your full name.'
        **kw   -- Optional allowed kw arguments are:
                  initial = None or str    Initial value of input field
        NEW  -->  strict  = True or False  Default is True, enforce strict boolean input.
                            If False, also allow the conversion of Yes, No, Y, N, 0, and 1
                            into True or False values.
                   parent  = None       The tkinter root window class to open the dialog from, 
                                        and return to after the dialog closes.
    RETURNS: a bool value or None
    '''
    result = multitypedialog(title, prompt, bool, **kw)
    if result[0]:
        return result[1]
    else:
        return None

def asklist(title, prompt, **kw):
    '''get a list value from the user

    ARGUMENTS:
        
        title   -- Is the dialog windows title as string, ie 'String Input Required.'
        prompt  -- Is the request label text as string, ie 'Please enter your full name.'
        **kw    -- Optional allowed kw arguments are:
                   initial = None or str  value of input field (depending on reqtype)
        NEW  -->   minval  = None or int  min value of input field (for numeric requests)
        NEW  -->   maxval  = None or int  Max value of input field (for numeric requests)
        NEW  -->   maxlen  = None or int  Max length of input allowed (for str and bytes)
        NEW  -->   minlen  = None or int  Min length of input required (for str and bytes)

                   parent  = None       The tkinter root window class to open the dialog from, 
                                        and return to after the dialog closes.
    RETURNS: a list value or None
    '''
    result = multitypedialog(title, prompt, list, **kw)
    if result[0]:
        return result[1]
    else:
        return None

def asktuple(title, prompt, **kw):
    '''get a tuple value from the user

    ARGUMENTS:
        
        title   -- Is the dialog windows title as string, ie 'String Input Required.'
        prompt  -- Is the request label text as string, ie 'Please enter your full name.'
        **kw    -- Optional allowed kw arguments are:
                   initial = None or str  value of input field (depending on reqtype)
        NEW  -->   minval  = None or int  min value of input field (for numeric requests)
        NEW  -->   maxval  = None or int  Max value of input field (for numeric requests)
        NEW  -->   maxlen  = None or int  Max length of input allowed (for str and bytes)
        NEW  -->   minlen  = None or int  Min length of input required (for str and bytes)

                   parent  = None       The tkinter root window class to open the dialog from, 
                                        and return to after the dialog closes.
    RETURNS: a tuple value or None
    '''
    result = multitypedialog(title, prompt, tuple, **kw)
    if result[0]:
        return result[1]
    else:
        return None

def askset(title, prompt, **kw):
    '''get a set value from the user

    ARGUMENTS:
        
        title   -- Is the dialog windows title as string, ie 'String Input Required.'
        prompt  -- Is the request label text as string, ie 'Please enter your full name.'
        **kw    -- Optional allowed kw arguments are:
                   initial = None or str  value of input field (depending on reqtype)
        NEW  -->   minval  = None or int  min value of input field (for numeric requests)
        NEW  -->   maxval  = None or int  Max value of input field (for numeric requests)
        NEW  -->   maxlen  = None or int  Max length of input allowed (for str and bytes)
        NEW  -->   minlen  = None or int  Min length of input required (for str and bytes)

                   parent  = None       The tkinter root window class to open the dialog from, 
                                        and return to after the dialog closes.
    RETURNS: a set value or None
    '''
    result = multitypedialog(title, prompt, set, **kw)
    if result[0]:
        return result[1]
    else:
        return None

def askdict(title, prompt, **kw):
    '''get a dict object from the user

    ARGUMENTS:
        
        title   -- Is the dialog windows title as string, ie 'String Input Required.'
        prompt  -- Is the request label text as string, ie 'Please enter your full name.'
        **kw    -- Optional allowed kw arguments are:
                   initial = None or str  value of input field (depending on reqtype)
        NEW  -->   minval  = None or int  min value of input field (for numeric requests)
        NEW  -->   maxval  = None or int  Max value of input field (for numeric requests)
        NEW  -->   maxlen  = None or int  Max length of input allowed (for str and bytes)
        NEW  -->   minlen  = None or int  Min length of input required (for str and bytes)

                   parent  = None       The tkinter root window class to open the dialog from, 
                                        and return to after the dialog closes.
    RETURNS: a dict object or None
    '''
    result = multitypedialog(title, prompt, dict, **kw)
    
    if result[0]: #converted ok
        return result[1]
    return None

def askbytes(title, prompt, **kw):
    '''get a bytes object from the user

    ARGUMENTS:
        
        title   -- Is the dialog windows title as string, ie 'String Input Required.'
        prompt  -- Is the request label text as string, ie 'Please enter your full name.'
        **kw    -- Optional allowed kw arguments are:
                   initial =  None or str   Value of input field (depending on reqtype)
        NEW  -->   maxlen  =  None or int   Max length of input allowed
        NEW  -->   minlen  =  None or int   Min length of input required
        NEW  -->   illegals = None or list  List of illegal characters

                   parent =  None           The tkinter root window class to open the dialog 
                                            from, and return to after the dialog closes.

    RETURNS: a bytes object or None
    '''
    if 'gethex' in kw and kw['gethex']:
        result = multitypedialog(title, prompt, str, **kw)
    else:
        result = multitypedialog(title, prompt, bytes, **kw)
    if result[0]:
        return result[1]
    else:
        return None

def askbytearray(title, prompt, **kw):
    '''get a bytearray object from the user

    ARGUMENTS:
        
        title   -- Is the dialog windows title as string, ie 'String Input Required.'
        prompt  -- Is the request label text as string, ie 'Please enter your full name.'
        **kw    -- Optional allowed kw arguments are:
                   initial =  None or str   Value of input field (depending on reqtype)
        NEW  -->   maxlen  =  None or int   Max length of input allowed
        NEW  -->   minlen  =  None or int   Min length of input required
        NEW  -->   illegals = None or list  List of illegal characters

                   parent =  None           The tkinter root window class to open the dialog 
                                            from, and return to after the dialog closes.

    RETURNS: a bytearray object or None
    '''
    if 'gethex' in kw and kw['gethex']:
        result = multitypedialog(title, prompt, str, **kw)
    else:
        result = multitypedialog(title, prompt, bytearray, **kw)
    
    if result[0]:
        return result[1]
    else:
        return None

"""asknonetuple returns either a 3 or 4 part tuple"""
def asknonetuple(title, prompt, **kw):
    '''get a None type object from the user

    ARGUMENTS:

        title   -- the dialog title
        prompt  -- the label text
        **kw    -- optional allowed kw arguments are:
                   initial = None or str  value of input field (depending on reqtype)
        NEW  -->   maxlen  = None or int  Max length of input allowed (for str and bytes)
        NEW  -->   strict  = True or False  Default is True, enforce strict 'None' inputs.
                             If False, also allow the conversion of 'null', 'nil' and '' into
                             a None type object.
                             
                   parent  = None       The tkinter root window class to open the dialog from, 
                                        and return to after the dialog closes.
                                        
    RETURNS: a 3 part tuple: (True, convertedInput, convertedType) if converted OK, or
             a 3 part tuple: (False, originalInput, originalType) if not passed limitations, or
    ON ERROR: returns a 4 part tuple: (None, originalInput, originalType, errorString)
    '''
    result = multitypedialog(title, prompt, None, **kw)
    return result

"""askmultitype returns a single value"""
def askmultitype(title, prompt, reqType, **kw):
    '''get a wide variety of type types from the user

    ARGUMENTS:
    
        title   - Is the dialog windows title as string, ie 'Enter a string.'
        prompt  - Is the request label text as string, ie 'Please enter your full name.'
        reqtype - str, int, float, bool, list, tuple, set, dict, bytes, bytearray, and None
        
        **kw    - optional allowed kw arguments are:
                  initial  str or None  # Initial value of input field (for all types)
        NEW  -->  subtype  'pw', 'email' or None  # enforce the subtype processing
        NEW  -->  show     '*' or None  # Show a '*' instead of each input char
        NEW  -->  minval   int or None  # Minimum value of input field (for numeric requests)
        NEW  -->  maxval   int or None  # Maximum value of input field (for numeric requests)
        NEW  -->  maxlen   int or None  # Maximum length (count of chars or collection items)
        NEW  -->  minlen   int or None  # Maximum length (count of chars or collection items)
        NEW  -->  mincap   int or None  # Minimum number of capital letters required
        NEW  -->  minnum   int or None  # Minimum number of numbers required
        NEW  -->  minsym   int or None  # Minimum number of symbols required. 
                                          Use illegals to specify and bad password chars
        NEW  -->  illegals list or None # List of illegal chars or strings in the input
        NEW  -->  regex    raw or None  # A raw (r'') regex string to validate the input with.
        NEW  -->  logval   bool or None # don't show value in the onedialog log. ie passwords
        NEW  -->  gethex   bool or None # Return input string as a hex string
        NEW  -->  strict   bool or None # Defaults True, enforce strict True or False inputs.
                  (for bool)              If strict is False, also allow the conversion of 
                                          Yes, No, Y, N, 0, and 1 into True or False values.
        NEW  -->  strict   bool or None # Defaults True, enforce strict 'None' inputs.
                  (for None)              If False, also allow the conversion of 
                                          'null', 'nil' and '' into a None object.
                  parent   root or None # The tkinter root window class link the dialog to, 
                                          and return to after the dialog closes.
        
    RETURNS: The input value of requested type, or None if it had a problem.
    '''
    result = multitypedialog(title, prompt, reqType, **kw)
    if result[0]:
        return result[1]
    else:
        return None

"""askmultitypetuple returns either a 3 or 4 part tuple"""
def askmultitypetuple(title, prompt, reqType, **kw):
    '''ask for a wide variety of input types from the user

    ARGUMENTS:
    
        title   - Is the dialog windows title as string, ie 'Enter a string.'
        prompt  - Is the request label text as string, ie 'Please enter your full name.'
        reqtype - str, int, float, bool, list, tuple, set, dict, bytes, bytearray, and None
        
        **kw    - optional allowed kw arguments are:
                  initial  str or None  # Initial value of input field (for all types)
        NEW  -->  subtype  'pw', 'email' or None  # enforce the subtype processing
        NEW  -->  show     '*' or None  # Show a '*' instead of each input char
        NEW  -->  minval   int or None  # Minimum value of input field (for numeric requests)
        NEW  -->  maxval   int or None  # Maximum value of input field (for numeric requests)
        NEW  -->  maxlen   int or None  # Maximum length (count of chars or collection items)
        NEW  -->  minlen   int or None  # Maximum length (count of chars or collection items)
        NEW  -->  mincap   int or None  # Minimum number of capital letters required
        NEW  -->  minnum   int or None  # Minimum number of numbers required
        NEW  -->  minsym   int or None  # Minimum number of symbols required. 
                                          Use illegals to specify and bad password chars
        NEW  -->  illegals list or None # List of illegal chars or strings in the input
        NEW  -->  regex    raw or None  # A raw (r'') regex string to validate the input with.
        NEW  -->  logval   bool or None # don't show value in the onedialog log. ie passwords
        NEW  -->  gethex   bool or None # Return input string as a hex string
        NEW  -->  strict   bool or None # Defaults True, enforce strict True or False inputs.
                  (for bool)              If strict is False, also allow the conversion of 
                                          Yes, No, Y, N, 0, and 1 into True or False values.
        NEW  -->  strict   bool or None # Defaults True, enforce strict 'None' inputs.
                  (for None)              If False, also allow the conversion of 
                                          'null', 'nil' and '' into a None object.
                  parent   root or None # The tkinter root window class link the dialog to, 
                                          and return to after the dialog closes.
        
    RETURNS: a 3 part tuple: (True, convertedInput, convertedType) if converted OK, or
             a 3 part tuple: (False, originalInput, originalType) if not passed limitations, or
    ON ERROR: returns a 4 part tuple: (None, originalInput, originalType, errorString)
    '''
    # converted, answer, answerType = multitypedialog(title, prompt, reqType, **kw)
    result = multitypedialog(title, prompt, reqType, **kw)
    return result


if __name__ == "__main__":

    def test():
        root = Tk()
        def doit(root=root):
            d = onedialog(root,
                         text="This is onedialog. "
                              "It is the swiss army knife of input dialogs, "
                              "and designed to be a drop in replacement for "
                              "tkinters.simpledialog.\n"
                              "Do you believe this?",
                         buttons=["Yes", "No", "Cancel"],
                         default=0,
                         cancel=2,
                         title="onedialog")
                         # master, text='', buttons=[], default=None, 
                         # cancel=None, title=None, class_=None
            
            print(d.go())
            
            logger.info(askstring("String", "Enter a string", 
                            initial='Ho"l\'low',
                            minlen=1, 
                            maxlen=50,
                            illegals=['"', "'", '\\', 'ast.', 'eval(', 
                                      'exec(', '__', 'sys.exit(', 
                                      'os.', '.destroy('],
                            regex=r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                            parent=root))
            print()
            logger.info(askpassword("Password", "Enter your password", 
                            initial='Hol1owWorld!',
                            show='*',
                            minlen=8,
                            maxlen=20,
                            mincap=1,
                            minlow=2,
                            minnum=1,
                            minsym=1,
                            illegals=[' ', '"', '=', "'", '\\'],
                            logval=False,
                            gethex=True,
                            parent=root))
            print()
            logger.info(askemailaddress("Email Address", "Enter your email address", 
                            initial='your.name@yahoo.com.au',
                            minlen=8, 
                            maxlen=40,
                            regex=r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                            parent=root))
            print()
            # ~ logger.info(askbytes("String to bytes", "Enter a string", 
                            # ~ initial='Hollow World',
                            # ~ minlen=1,
                            # ~ maxlen=15,
                            # ~ gethex=False,
                            # ~ parent=root))
            # ~ print()
            # ~ logger.info(askbytearray("String to bytearray", "Enter a string", 
                            # ~ initial='Hollow World',
                            # ~ minlen=1,
                            # ~ maxlen=15,
                            # ~ gethex=False,
                            # ~ parent=root))
            # ~ print()
            # ~ logger.info(askinteger("Integer", "Enter a Integer", 
                            # ~ initial=-45, 
                            # ~ minval=-50, 
                            # ~ maxval=50,
                            # ~ parent=root))
            # ~ print()
            # ~ logger.info(askfloat("Float", "Enter a float",
                            # ~ initial=00041.9785, 
                            # ~ minval=0.0, 
                            # ~ maxval=50.0,
                            # ~ parent=root))
            # ~ print()
            # ~ logger.info(askbool("Bool", "Enter a bool", 
                            # ~ initial='1', 
                            # ~ strict=False,
                            # ~ parent=root))
            # ~ print()
            # ~ logger.info(asklist("List", "Enter a list", 
                            # ~ initial="['Hollow', 'World']",
                            # ~ minitems=1,
                            # ~ maxitems=2,
                            # ~ types=[str, int, float, bool], # list of allowed types
                            # ~ walk=True, # walk all child items checking security issues.
                            # ~ parent=root))
            # ~ print()
            # ~ logger.info(asknonetuple("None", "Enter a 'None' value", 
                            # ~ initial='null', 
                            # ~ strict=False,
                            # ~ parent=root))
            print()
            logger.info(askmultitype("Password", "Enter your password", str, 
                            initial='Hol1owWorld!', # initial input string value
                            subtype='pw', # force the password sub process.
                            minval=-50, # irrelevant in this case and will be ignored
                            maxval=50, # irrelevant in this case and will be ignored
                            minlen=8, # Minimum length of chars or items required.
                            maxlen=20, # maximum length of chars or items  allowed.
                            mincap=1, # Minimum number of capitals required in string.
                            minlow=2, # Minimum number of lowercase required in string.
                            minnum=1, # Minimum number of numbers  required in string.
                            minsym=1, # Minimum number of symbols required in string.
                            show='*', # Show '*' instead of input chars (for passwords)
                            logval=False, # don't show passwords in the onedialog log file.
                            gethex=True, # Return input string as a hex string
                            illegals=[' ', '"', '=', "'", '\\'], # List of illegal input (chars or strings)
                            regex = None, #r'', # A raw (r'') regex string used to validate input.
                            walk=True, # walk all child items checking security issues.
                            types=[str, int, float, bool], # list of allowed types in collections
                            parent=root)) # A <tkinter.Tk object .>
            # ~ print()
            # ~ logger.info(askmultitypetuple("List", "Enter a List", list, 
                            # ~ initial="['Hollow', 'World']",
                            # ~ minitems=2,
                            # ~ maxitems=3,
                            # ~ types=[str, int, float, bool], # list of allowed types
                            # ~ walk=True, # walk all child items checking security issues.
                            # ~ parent=root))
            # ~ print()
            # ~ logger.info(askmultitypetuple("Dictionary", "Enter a dict", dict, 
                            # ~ initial="{0: 0, 1: '1', 2: True,  3: ['bad']}",
                            # ~ minitems=1, # Minimum number of items required.
                            # ~ maxitems=4, # Maximum number of items allowed.
                            # ~ walk=True, # walk all child items checking security issues.
                            # ~ types=[str, int, float, bool], # list of allowed types
                            # ~ parent=root))
            # ~ print()
            # ~ logger.info(askmultitypetuple("Set", "Enter a set", set, 
                            # ~ initial="{'Hollow', 'World'}",
                            # ~ minitems=1, # Minimum number of items required.
                            # ~ maxitems=3, # Maximum number of items allowed.
                            # ~ types=[str, int, float, bool], # list of allowed types
                            # ~ parent=root))
            # ~ try:
                # ~ print()
                # ~ logger.info(askmultitypetuple("Testing Forced Error", "Forcing Error", frozenset, 
                            # ~ initial="Hollow, World",
                            # ~ parent=root))
            # ~ except (NameError):
                # ~ logger.exception("Unsupported request type.")

        t = Button(root, text='Test', command=doit)
        t.pack()
        q = Button(root, text='Quit', command=t.quit)
        q.pack()
        t.mainloop()
    
    test()
