#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  pysist.py
#  
#  2020 Wharpusware <wharpus@gmail.com>
#  
# Python program to illustrate the usage 
# of hierarchical treeview with scrollbars in python GUI 
# application using tkinter 

import os
import sys

try:
    import tkinter as tk #python3
except ImportError as err:
    print('Pysist requires Python 3.#.')
    print('Import Error: {}'.format(err))
    sys.exit(0)

from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
from tkinter.colorchooser import askcolor
from tkfilebrowser import askopendirname, askopenfilename, asksaveasfilename

import time
import json
import uuid
import platform
from dotmap import DotMap
from copy import deepcopy


class B:
    
    # Make sure CWD is set correctly
    PATH_TO_ME = os.path.dirname(os.path.abspath(__file__))
    os.chdir(PATH_TO_ME)
    CWD = os.getcwd()
    
    # App constants
    _APP_NAME = "Pysist" # Hard coded Constant
    VERSION = "0.0.1" # Hard coded Constant
    VERSION_LIST = VERSION.split(".")
    OP_SYSTEM_TYPE = platform.system()
    USER_NAME = os.getlogin()
    USER_HOME_PATH = os.path.expanduser("~")
    print("Welcome to '{}' v{}".format(_APP_NAME, VERSION))
    print("Designed and created by Wharpus Ware <wharpus@gmail.com>")
    print("{} is located in {}".format(_APP_NAME, CWD))
    print()
    
    # Immutable default root (R_) constants
    R_DEFAULT_DIR = "./"
    R_DEFAULT = "root.json"
    R_DEFAULT_TYPE = "json"
    R_DEFAULT_PATH = os.path.join(R_DEFAULT_DIR, R_DEFAULT)
    
    # Immutable startup store (S_) constants
    S_DIR = "./" # Path and name of startup folder
    S_FILE = "startup.json" # Can include path
    S_TYPE = "json" # 'json', 'sqlite3' or 'dict'
    S_KEY = None # Dict key, SQL table name or None
    S_PATH = os.path.join(S_DIR, S_FILE)
    
    # Immutable data store (D_) constants.
    D_DIR = "./data" # Path and name of data folder
    D_FILE = "root.sqlite"
    D_TYPE = "sqlite3"
    D_KEY = "data" # Sqlite table name
    D_PATH = os.path.join(D_DIR, D_FILE)
    
    # Below are either dict key names (strings), or a list index number
    # Immutable treeview constants
    _T_VALS = "columns" # Dict key name of column values
    _T_DISP_VAL = 0 # list index of 1st column (item value)
    _T_DISP_KIND = 1  # list index of 2nd column (item kind)
    _T_DISP_3 = 2  # list index of 3rd column (item ?)
    _T_OPEN = "isopen" # Dict key name of a isopen value
    _T_ROWTYPE = "rowtype" # Dict key name of a rowtype value
    _T_PARENT = "parent" # Dict key name of a parent value
    _T_POS = "position" # Dict key name of a position value
    _T_TAGS = "tags" # Dict key name of a tags value
    _T_NAME = "text" # Dict key name of main tree items (column #0)
    _T_UID = "uid" # Dict key name of a uid value

    # Mutable root file specs (R_) semi constants.
    R_DIR = R_DEFAULT_DIR # Uses startup's 'lastRootPath' value.
    R_FILE = R_DEFAULT # Uses startup's 'lastRoot' value.
    R_TYPE = R_DEFAULT_TYPE # Uses startup's 'lastRootType' value.
    R_PATH = R_DEFAULT_PATH # Build from R_DIR and R_FILE

    # Mutable Local Storage
    nodes = None
    prefs = None
    PREFS = None
    S_PREFS = None # Filled on startup from ./startup.json
    TREEROOT = None # Uses R_DIR, R_FILE, R_TYPE loaded from S_PREFS
    R_PREFS = None # Loaded from TREEROOT using P_KEY from S_PREFS
    R_NODES = None # Loaded from TREEROOT using N_KEY from R_PREFS
    R_THEMES = None
    
    # Mutable prefs store (P_) semi constants. Uses startup's 'prefsKey' value
    P_KEY = "prefs"
    
    # Mutable node store (N_) semi constants. Uses startup 'nodeKey' value
    N_KEY = "nodes" # Dict key, or SQL table or None
    
    # define required system flags
    flDirtyRoot = False # used to notify if root data has changed
    flDirtyPrefs = False # used to notify if Prefs data has changed
    flStartingUp = False # used to notify if app is still starting up
    flShutdownNow = False # if True notify the app to start the shutdown process
    flShuttingDown = False # used to notify if app is shutting down up

    # Just some node data to save if required
    R_DEFAULT_NODES = dict({
                            "root": {
                              "rowtype": "Root",
                              "columns": [
                                "2 items",
                                "table Root"
                              ],
                              "isopen": True,
                              "parent": "",
                              "position": 0,
                              "tags": "R",
                              "text": "ROOT",
                              "uid": "root",
                              "value": "2 items",
                              "type": "table",
                              "ref": ""
                            },
                            "d1": {
                              "rowtype": "Table",
                              "columns": [
                                "1 item",
                                "child Table"
                              ],
                              "isopen": True,
                              "parent": "root",
                              "position": "end",
                              "tags": "T",
                              "text": "User",
                              "uid": "d1",
                              "value": "1 item",
                              "type": "child",
                              "ref": ""
                            },
                            "d2": {
                              "rowtype": "Table",
                              "columns": [
                                "1 item",
                                "child Table"
                              ],
                              "isopen": True,
                              "parent": "root",
                              "position": "end",
                              "tags": "T",
                              "text": "System",
                              "uid": "d2",
                              "value": "1 item",
                              "type": "child",
                              "ref": ""
                            },
                            "v1": {
                              "rowtype": "var",
                              "columns": [
                                "root.json",
                                "STR var"
                              ],
                              "isopen": False,
                              "parent": "d1",
                              "position": "end",
                              "tags": "v",
                              "text": "myName",
                              "uid": "v1",
                              "value": "root.json",
                              "type": "str",
                              "ref": ""
                            },
                            "v2": {
                              "rowtype": "var",
                              "columns": [
                                "I'm a string",
                                "STR var"
                              ],
                              "isopen": False,
                              "parent": "d2",
                              "position": "end",
                              "tags": "v",
                              "text": "sampleVariable",
                              "uid": "v2",
                              "value": "I'm a string",
                              "type": "str",
                              "ref": ""
                            }
                        })

    _type_map = {
        'bash': ['script', 'utf-8'],
        'bmp': ['image', 'bytes'],
        'bool': ['var', 'utf-8'],
        'bytearray': ['var', 'bytes'],
        'bytes': ['var', 'bytes'],
        'cfg': ['file', 'utf-8'],
        'cgi': ['script', 'utf-8'],
        'cmd': ['script', 'utf-8'],
        'com': ['script', 'utf-8'],
        'complex': ['var', 'utf-8'],
        'conf': ['file', 'utf-8'],
        'config': ['file', 'utf-8'],
        'css': ['file', 'utf-8'],
        'csv': ['file', 'utf-8'],
        'dict': ['var', 'utf-8'],
        'float': ['var', 'utf-8'],
        'frozenset': ['var', 'utf-8'],
        'gif': ['image', 'bytes'],
        'glade': ['file', 'utf-8'],
        'gui': ['file', 'utf-8'],
        'htm': ['file', 'utf-8'],
        'html': ['file', 'utf-8'],
        'ico': ['image', 'bytes'],
        'ini': ['file', 'utf-8'],
        'int': ['var', 'utf-8'],
        'java': ['script', 'utf-8'],
        'jpeg': ['image', 'bytes'],
        'jpg': ['image', 'bytes'],
        'js': ['script', 'utf-8'],
        'jscript': ['script', 'utf-8'],
        'jsf': ['file', 'utf-8'],
        'list': ['var', 'utf-8'],
        'md': ['file', 'utf-8'],
        'memoryview': ['var', 'bytes'],
        'pcgi': ['script', 'utf-8'],
        'pdf': ['file', 'bytes'],
        'pic': ['image', 'bytes'],
        'pl': ['script', 'utf-8'],
        'png': ['image', 'bytes'],
        'proj': ['file', 'utf-8'],
        'proot': ['file', 'utf-8'],
        'ps1': ['script', 'utf-8'],
        'ps1xml': ['file', 'utf-8'],
        'psd1': ['file', 'utf-8'],
        'psm1': ['script', 'utf-8'],
        'py': ['script', 'utf-8'],
        'py2': ['script', 'utf-8'],
        'py3': ['script', 'utf-8'],
        'py4': ['script', 'utf-8'],
        'pysist': ['file', 'utf-8'],
        'range': ['var', 'utf-8'],
        'root': ['file', 'utf-8'],
        'set': ['var', 'utf-8'],
        'sh': ['script', 'utf-8'],
        'str': ['var', 'utf-8'],
        'svg': ['image', 'utf-8'],
        'text': ['var', 'utf-8'],
        'tsv': ['file', 'utf-8'],
        'tuple': ['var', 'utf-8'],
        'txt': ['file', 'utf-8'],
        'ui': ['file', 'utf-8'],
        'xml': ['file', 'utf-8'],
        'yaml': ['file', 'utf-8']
        }
    
    _row_types = ["Root", "Table", "Dir", "file", "text", "var", 
                "image", "bytes", "script", "code", "none"]
                    
    _table_types = ['Table', 'Root', 'Dir']
    
    _file_types = ['file', 'script']
    
    _var_types = ['var', 'str', 'bool', 'int', 'float', 'dict', 'list', 'tuple', 
                'bytes', 'bytearray', 'complex', 'frozenset', 'set', 'range', 'None']
                    
    _special_var_types = ['text', 'script', 'code', 'address', 'filespec', 'path', 'image', 'none']
    
    _script_types = ['script']

    _code_types = ['code']


class Window(tk.Toplevel, B):

    def __init__(self, root, args=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "'self', '{}', {}".format(root, args)))
        self.root = root
        self.args = args
        
        if args is not None:
            self.flDebug = args.debug
            self.flTest = args.test
            self.flNoWindow = args.window
            self.use_startup = args.startup
            self.use_root = args.root

            if args.startup is not None:
                if os.path.isfile(args.startup):
                    self.use_startup = args.startup
                else:
                    print("Could not find startup file at {}".format(args.startup))
                    self.use_startup = ask_open_startup()
                    print (self.use_startup)

            if args.root is not None:
                if os.path.isfile(args.root):
                    self.use_root = args.root
                else:
                    print("Could not find root file at {}".format(args.root))
                    self.use_root = self.ask_open_root()
        else:
            self.flDebug = False
            self.flTest = False
            self.flNoWindow = False
            self.use_startup = None
            self.use_root = None
        
        if self.flDebug:
            print("Debug mode enabled")
        if self.flTest:
            print("Testing mode enabled")
        if self.flNoWindow:
            print("Windowless mode enabled")
        if self.use_startup is not None:
            print("Using startup file at {}".format(self.use_startup))
        else:
            print("Using the default startup file.")
        if self.use_root is not None:
            print("Using root file at {}.".format(self.use_root))
        else:
            print("Using the default last used root file.")
                
        # perform the build process
        self.do_startup()
        self.add_menubar()
        self.build_styles()
        self.add_scrollbars()
        self.init_treeview()
        self.apply_tree_columns()
        self.create_tags()
        self.build_treeview()
        self.control_scrollbars()
        self.create_bindings()

    def do_startup(self):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            'self'))
        # ~ xx = ["Root", "Table", "Dir", "file", "text", "var", "image", "bytes", "code", "none"]
        # ~ print('The index of "text" is {}'.format(xx.index("text")))

        # Init startup prefs (B.PREFS) with defaults values
        self.init_startup_PREFS(B.S_PATH, B.S_TYPE, B.S_KEY)

        # Load 'startup.json' and merge it with default startup prefs
        self.get_startup_PREFS(B.S_PATH, B.S_TYPE, B.S_KEY)

        # Init default node prefs dict (B.prefs) with default values
        self.init_node_prefs()
        
        # Open last used root and load nodes and prefs over default node and prefs
        self.get_root(B.R_PATH, B.R_TYPE, B.P_KEY, B.N_KEY)

    def init_startup_PREFS(self, FILE='./startup.json', TYPE='json', KEY=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, '{}', '{}', '{}'".format(FILE, TYPE, KEY)))
        B.PREFS = {
            "autoSaveInterval": 5, # Must save
            "backupExt": ".bak", # Allow user access
            "backupDirName": "./backups", # Allow user access
            "dataDirName": "./data",
            "dataStoreType": "sqlite3",
            "dataStoreName": "root.sqlite",
            "dataKey": "data", # Sqlite table name
            "flAutoSave": False, # Allow user access
            "flAutoSaveOnChange": True, # Allow user access
            "flAutoSaveOnClose": True, # Allow user access
            "flEnableAgents": True, # Allow user access
            "flEnableWebServer": False, # Allow user access
            "flErrorLogs": True, # Allow user access
            "flFirstStartup": True, # Must save
            "flNightlyBackups": False, # Allow user access
            "flWebErrorLogs": True, # Allow user access
            "flWebLogs": False, # Allow user access
            "flWebStats": True, # Allow user access
            "lastBackupCount": 0, # Must save
            "lastBackupName": "", # User information
            "lastBackupDate": "", # User information
            "lastRoot": "root.json", # Must save
            "lastRootPath": "./", # Use this root path
            "lastRootType": "json", # Must save
            "logDirName": "./logs", # Allow user access
            "nodeKey": "nodes",
            "openBrowserCommand": "firefox {}", # Allow user access
            "prefsKey": "prefs",
            "recentRoots": ["./root.json"], # Must save with path
            "webCGIext": ".pcgi",
            "webHomePage": "index.html", # Allow user access
            "webServerHostName": "localhost:8080", # Allow user access
            "webServerPorts": [8080, 8081], # Allow user access
            "webSiteDirName": "./www" # Allow user access
        }
        
        # If startup.json file doesn't exist, create default startup.json file 
        if not os.path.isfile(FILE):
            print('The {} startup file does not exist, creating it...'.format(FILE))
            if TYPE == 'json':
                # Save startup.json file with default data
                with open(FILE, 'w') as outfile:
                    print('Writing startup PREFS to: {}'.format(FILE))
                    if KEY is None: # Save PREFS data as is (without a dict key)
                        json.dump(B.PREFS, outfile, sort_keys=True, ensure_ascii=True, indent=2)
                    else:
                        data = dict()
                        data[KEY] = B.PREFS
                        json.dump(data, outfile, sort_keys=True, ensure_ascii=True, indent=2)
                        
        self.update_constants()
        
    def get_startup_PREFS(self, FILE='./startup.json', TYPE='json', KEY=None):
        print("{}: {}({})".format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, '{}', '{}', '{}'".format(FILE, TYPE, KEY)))
        
        if TYPE == 'sqlite3':
            print('NOTE: sqlite3 startup prefs are NOT YET SUPPORTED.')
            print('NOTE: Using default FILE, TYPE, and KEY values.')
            FILE = B.S_PATH
            TYPE = B.S_TYPE
            KEY = B.S_KEY
        
        # print("Reading startup file from: '{}'".format(FILE))
        
        # Read in and merge the startup file
        if TYPE == 'json':
            with open(FILE) as startup_file:
                startup = json.load(startup_file) # Startup dict
                if KEY is not None: # Load startup data using startup key 
                    startup = startup[KEY]

                '''
                S_PREFS should be a ref to PREFS, NOT a hard copy, 
                so that S_PREFS changes when PREFS does. 
                PREFS can change after loading startup.json
                Merge current PREFS with startup.json data.
                '''
                B.PREFS = self.merge_dicts(B.PREFS, startup)
                self.update_constants()
        
    def init_node_prefs(self):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            'self'))

        B.prefs = {}
        B.prefs['colNames'] = ['#0', '#1', '#2']
        B.prefs['colHeads'] = ['Name', 'Value', 'Kind']
        B.prefs["colStretch"] = [False, True, False]
        B.prefs['colMinWidths'] = [160, 120, 100]
        B.prefs['colWidths'] = [200, 250, 100]
        B.prefs["rowTypes"] = ["Root", "Table", "Dir", "file", "text", 
                                "var", "image", "bytes", "script", "code", "none"] # Case matters
        B.prefs["tagNames"] = ["R", "T", "D", "f", "t", 
                                "v", "i", "b", "s","c", "n"] # Case matters
        B.prefs["tagBg"] = ["#DDB3B3", "#F0CFCF", "#F0CFCF", "#F8F8F8", "#F8F8F8", 
                            "#9EEEEB", "#A5E0F5", "#E2E389", "#F8F8F8", "#F8F8F8", "#FFFFFF"]
        B.prefs['rootGeo'] = "+56+28"
        B.prefs['rootTitle'] = "Pysist {}"
        B.prefs['topNodeUid'] = "root"
        B.prefs['fileFormat'] = 1.1
        
        self.update_constants()

    # Auto load last root file used
    def get_root(self, FILE='./root.json', TYPE='json', P_KEY='prefs', N_KEY='nodes'):
        print("{}: {}({})".format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, '{}', '{}', '{}', '{}'".format(FILE, TYPE, P_KEY, N_KEY)))
        
        if not os.path.isfile(FILE): # Check again with default values
            print("Can't find your latest root file: {}...".format(FILE))

            FILE = B.R_DEFAULT_PATH
            print("Root file path: '{}'".format(FILE))
            TYPE = B.R_DEFAULT_TYPE

            print("Looking for the default root file: '{}'".format(FILE))
            # **** TO-DO **** #
            # Show askOpenFileDialog()
            
            if not os.path.isfile(FILE): # Check again with default values
                print("Can't find the default root file: '{}'".format(FILE))
                # **** TO-DO **** #
                # Show askOpenFileDialog()
                print("Creating the default root file named: '{}'".format(FILE))
            
                
                # The new root must contain both the default nodes and prefs.
                newRootData = {}
                newRootData[N_KEY] = B.R_DEFAULT_NODES
                newRootData[P_KEY] = B.prefs
                
                # Save data to root.json file
                if TYPE == 'json':
                    with open(FILE, 'w') as outfile:
                        print("Writing default node prefs to: '{}'".format(FILE))
                        json.dump(newRootData, outfile, sort_keys=False, ensure_ascii=True, indent=2)
                else:
                    print('Unsupported Root file type.')

        if TYPE == 'json':
            with open(FILE) as json_file:
                B.TREEROOT = json.load(json_file) # now contains full root.json
                
            # Load node prefs from TREEROOT
            B.R_PREFS = B.prefs = self.merge_dicts(B.prefs, B.TREEROOT[P_KEY])
            #B.R_PREFS = B.prefs # just a reference to prefs

            # nodes is where we get and set all node changes
            B.R_NODES = B.nodes = B.TREEROOT[N_KEY]
            #R_NODES = B.nodes # just a reference to nodes
        else:
            print('Unsupported Root file type.')
        
        self.update_constants()
        
    def update_constants(self):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            'self'))
        # Mutable root file specs (R_) semi constants.
        B.R_DIR = B.PREFS['lastRootPath']
        B.R_FILE = B.PREFS['lastRoot']
        B.R_TYPE = B.PREFS['lastRootType']
        B.R_PATH = os.path.join(B.R_DIR, B.R_FILE)

        # Mutable prefs store (P_) semi constants. Uses startup's 'prefsKey' value
        B.P_KEY = B.PREFS["prefsKey"]
        
        # Mutable node store (N_) semi constants. Uses startup 'nodeKey' value
        B.N_KEY = B.PREFS["nodeKey"]
        
        # Mutable Local Storage
        B.S_PREFS = B.PREFS
        B.R_PREFS = B.prefs
        B.R_NODES = B.nodes
        B.TREEROOT = {} # clear TREEROOT dict
        B.TREEROOT[B.P_KEY] = B.R_PREFS
        B.TREEROOT[B.N_KEY] = B.R_NODES

    def add_menubar(self):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            'self'))
        # creates menu
        self.menubar = tk.Menu(self.root)

        # Create File Menu
        self.filemenu = filemenu = tk.Menu(self.menubar, takefocus=True, tearoff='false')
        filemenu.add('command', command=self.on_file_new_root, 
                     label='New root...', state='normal')
        filemenu.add('command', command=self.on_file_open_root, 
                     label='Open root...', state='normal', underline='0')
        filemenu.add('command', command=self.on_file_save_root, 
                     label='Save root', state='normal', underline='0', 
                     accelerator="Ctrl+S")
        filemenu.add('command', command=self.on_file_save_root_as, 
                     label='Save root as ...', state='normal', underline='10')
        filemenu.add('command', command=self.on_file_save_prefs, 
                     label='Save prefs', state='normal', accelerator="Shift+Ctrl+S")
        filemenu.add('command', command=self.on_file_backup_root, 
                     label='Backup root', state='normal', underline='0')
        filemenu.add('separator')
        filemenu.add('command', command=self.on_file_close_root, 
                     label='Close root', state='normal', underline='0')
        filemenu.add('command', command=self.on_file_quit, 
                     label='Quit', state='normal', underline='0', accelerator="Ctrl+Q")
        self.menubar.add(tk.CASCADE, menu=filemenu, label='File', 
                     state='normal', underline='0')
        # Create Edit Menu
        self.menu = editmenu = tk.Menu(self.menubar, takefocus=True, tearoff='false')
        editmenu.add('command', command=self.on_tree_copy, label='Copy', 
                     state='normal', accelerator="Ctrl+C")
        editmenu.add('command', command=self.on_tree_paste, label='Paste', state='normal', 
                     accelerator="Ctrl+V")
        editmenu.add('command', command=self.on_tree_cut, label='Cut', state='normal', 
                     accelerator="Ctrl+X")
        editmenu.add('command', command=self.on_tree_delete, label='Delete', state='normal', 
                     accelerator="Delete")
        editmenu.add('separator')
        editmenu.add('command', command=self.on_openSelected, label='Open Selected', state='normal', 
                     accelerator="Ctrl+O")
        editmenu.add('separator')
        editmenu.add('command', command=self.on_edit_root_prefs, label='Root Prefs ...', 
                     state='normal', underline='0')
        editmenu.add('command', command=self.on_edit_startup_prefs, label='Startup Prefs ...', 
                     state='normal', underline='0')
        self.menubar.add(tk.CASCADE, menu=editmenu, label='Edit', state='normal', underline='0')
        # Create New Menu
        self.newmenu = newmenu = tk.Menu(self.menubar, takefocus=True, tearoff='false')
        newmenu.add('command', command=self.on_new_table, label='Table type', 
                    state='normal', underline='0')
        newmenu.add('command', command=self.on_new_text, label='Text type', 
                    state='normal', underline='2')
        newmenu.add('command', command=self.on_new_outline, label='Outline type', 
                    state='normal', underline='0')
        newmenu.add('command', command=self.on_new_code, label='Code type', 
                    state='normal', underline='0')
        newmenu.add('command', command=self.on_new_image, label='Image type', 
                    state='normal', underline='1')
        newmenu.add('command', command=self.on_new_undefined, label='Undefined', 
                    state='normal', underline='0')
        newmenu.add('separator')
        newmenu.add('command', command=self.on_new_string, label='String var', 
                    state='normal', underline='0')
        newmenu.add('command', command=self.on_new_integer, label='Integer var', 
                    state='normal', underline='0')
        newmenu.add('command', command=self.on_new_float, label='Float var', 
                    state='normal', underline='0')
        newmenu.add('command', command=self.on_new_boolean, label='Boolean var', 
                    state='normal', underline='0')
        newmenu.add('command', command=self.on_new_dict, label='Dict var', 
                    state='normal', underline='0')
        newmenu.add('command', command=self.on_new_list, label='List var', 
                    state='normal', underline='0')
        newmenu.add('command', command=self.on_new_tuple, label='Tuple var', 
                    state='normal', underline='4')
        newmenu.add('command', command=self.on_new_set, label='Set var', 
                    state='normal', underline='1')
        newmenu.add('command', command=self.on_new_path, label='Path var', 
                    state='normal', underline='0')
        newmenu.add('command', command=self.on_new_address, label='Address var', 
                    state='normal', underline='0')
        newmenu.add('command', command=self.on_new_none, label='None var', 
                    state='normal', underline='0')
        self.menubar.add(tk.CASCADE, menu=newmenu, label='New', state='normal', underline='0')
        # Create View Menu
        self.viewmenu = viewmenu = tk.Menu(self.menubar, takefocus=True, tearoff='false')
        viewmenu.add('command', command=self.on_view_show_info, label='Show Info', 
                     state='normal', underline='5')
        self.menubar.add(tk.CASCADE, menu=viewmenu, label='View', state='normal', underline='0')
        # Create Dynamic User Menu
        self.usermenu = usermenu = tk.Menu(self.menubar, takefocus=True, tearoff='false')
        usermenu.add('command', command=self.on_user_add_bookmark, label='Add Bookmark', 
                     state='normal', underline='0')
        usermenu.add('command', command=self.on_user_bookmarks, label='Bookmarks...', 
                     state='normal', underline='0')
        self.menubar.add(tk.CASCADE, menu=usermenu, label='{}'.format(self.first_word(B.USER_NAME)), state='normal', underline='0')
        # Create Help Menu
        self.helpmenu = helpmenu = tk.Menu(self.menubar, takefocus=True, tearoff='false')
        helpmenu.add('command', command=self.on_help_about, label='About {}'.format(B._APP_NAME), 
                     state='normal', underline='0')
        helpmenu.add('command', command=self.on_help_online_help, label='Online Help', 
                     underline='0')
        self.menubar.add(tk.CASCADE, menu=helpmenu, label='Help', state='normal', underline='0')
        self.menubar.config(activebackground='#b3d9d9', background='#f0eef3', font='TkMenuFont', 
                    takefocus=True)
        self.root.config(menu=self.menubar)

    def build_styles(self):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            'self'))
        # Define the styles
        self.style = ttk.Style()
        # body font
        self.style.configure("mystyle.Treeview", highlightthickness=0, 
                            bd=0, font=('Calibri', 11))
        # heading font
        self.style.configure("mystyle.Treeview.Heading", 
                            font=('Calibri', 12,'bold'))
        # Remove borders
        self.style.layout("mystyle.Treeview", 
                        [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

    def add_scrollbars(self):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            'self'))
        # define the vertical and horizontal scrollbars
        self.SVBar = ttk.Scrollbar(self.root)
        self.SVBar.pack(side=tk.RIGHT, fill="y")
        self.SHBar = ttk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        self.SHBar.pack (side=tk.BOTTOM, fill="x")

    def init_treeview(self):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            'self'))
        # create the treeview with scrollbars
        self.tree = ttk.Treeview(self.root, style="mystyle.Treeview", 
                                yscrollcommand=self.SVBar.set, 
                                xscrollcommand=self.SHBar.set)
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
        self.root.title(B.prefs['rootTitle'].format(B.R_PATH))
        self.root.geometry(B.prefs['rootGeo'])  # W x H + Left + Top

    def apply_tree_columns(self):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            'self'))
        # Apply treeview columns and headings
        self.tree["columns"] = tuple(B.prefs['colNames'][1:])
        for x in range(len(B.prefs['colNames'])):
            self.tree.column(B.prefs['colNames'][x], width=B.prefs['colWidths'][x], 
                            minwidth=B.prefs['colMinWidths'][x], stretch=B.prefs['colStretch'][x])
            self.tree.heading(B.prefs['colNames'][x], text=B.prefs['colHeads'][x], anchor=tk.W)
            
    def create_tags(self):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            'self'))
        # Define some tags to use
        #print(B.prefs['tagNames'])
        for x in range(0, len(B.prefs['tagNames'])):
            tag = B.prefs['tagNames'][x]
            #print(tag)
            self.tree.tag_configure(B.prefs['tagNames'][x], background=B.prefs['tagBg'][x])

    def build_treeview(self, FILE='./root.json', TYPE='json', KEY='prefs'):
        print("{}: {}({})".format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, '{}', '{}', '{}'".format(FILE, TYPE, KEY)))
        xx = B.prefs["rowTypes"]
        tagList = B.prefs["tagNames"]
        
        # loop through all nodes and build tree
        for key in B.nodes:
            # print(key)
            rowtype = B.nodes[key][B._T_ROWTYPE]
            # print(rowtype)
            parent = B.nodes[key][B._T_PARENT]
            # print(parent)
            position = B.nodes[key][B._T_POS]
            # print(position)
            uid = B.nodes[key][B._T_UID]
            # print(uid)
            itemname = B.nodes[key][B._T_NAME]
            # print(itemname)
            itemcolumns = B.nodes[key][B._T_VALS]
            # print(itemcolumns)
            isopen = B.nodes[key][B._T_OPEN]
            # print(isopen)
            
            # Make sure the style tag is correct for rowtype
            typeitemlist = rowtype.split() # get the last word
            baseitem = typeitemlist[-1]
            subitem = typeitemlist[0]
            baseIndex = xx.index(baseitem)
            tag = tagList[baseIndex]
            #print("The tag for '{}' is {}".format(baseitem, tag))
            
            B.nodes[key][B._T_TAGS] = tag # Change it in B.nodes
            itemtags = tuple(B.nodes[key][B._T_TAGS]) # To tuple
            # print(itemtags, '\n')

            self.tree.insert(parent, position, uid, text=itemname, 
                        values=itemcolumns, open=isopen, tags=itemtags)
        
        # Pack everything into the window
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        if self.tree.selection() is (): # if empty select 'root'
            self.tree.focus('root')
            self.tree.selection_set('root')
        self.selected_items = self.tree.selection() # tuple
        # print('self.selected items:', self.selected_items)
        self.selected_data = {}
        for selected_uid in self.selected_items: # for multi selections
            # print('selected_uid: {}'.format(selected_uid))
            selected_item_data = self.tree.item(selected_uid) # dict of data
            # print('selected_item_data: {}'.format(selected_item_data))
            self.selected_data.update({selected_uid : selected_item_data}) # keyed dict
        # print('self.selected_data: {}'.format(self.selected_data))
        # ~ self.selections = self.tuple2list(self.selected_items) # list 
        # ~ #self.tree.selection_set(self.selections) # select all uids in list

    def control_scrollbars(self):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            'self'))
        # Control the treeview scrollbars
        self.SVBar.config(command=self.tree.yview)
        self.SHBar.config(command=self.tree.xview)

    def create_bindings(self):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            'self'))
        # Bind up a few things
        self.root.bind('<Control-q>', self.on_file_quit)
        self.tree.bind('<ButtonRelease-1>', self.on_selectItem)
        self.tree.bind('<Double-Button-1>', self.on_openSelected)
        self.tree.bind("<Return>", lambda e: self.on_openSelected())
        self.tree.bind('<Control-o>', self.on_openSelected)
        self.tree.bind('<Control-x>', self.on_tree_cut)
        self.tree.bind('<Control-c>', self.on_tree_copy)
        self.tree.bind('<Control-v>', self.on_tree_paste)
        self.tree.bind('<Delete>', self.on_tree_delete)
        self.tree.bind('<ButtonPress-3>', self.on_showContexMenu)
        self.tree.bind('<ButtonRelease-3>', self.on_doContexMenu)
        # self.tree.bind('<ButtonPress-1>', self.on_selectItem)
        # self.tree.bind('<Triple-Button-1>', self.on_open_selected)

    def update_window_stats(self):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            'self'))
        self.update()
        # ~ prefs.rootWidth = self.root.winfo_width()
        # ~ prefs.rootHeight = self.root.winfo_height()
        B.prefs.rootGeo = str(self.root.winfo_geometry())
        cols = ('#0', ) + self.tree.cget('columns')  # tuple of all columns
        B.prefs.colNames = self.tuple2list(cols)  # overwite colNames with a list
        B.prefs.colWidths = []  # Remove defaults
        B.prefs.colMinWidths = []  # Remove defaults
        B.prefs.colHeads = []  # Remove defaults
        for colName in B.prefs.colNames:
            B.prefs.colWidths.append(self.tree.column(colName, 'width'))
            B.prefs.colMinWidths.append(self.tree.column(colName, 'minwidth'))
            B.prefs.colHeads.append(self.tree.heading(colName, 'text'))

    def get_theme_tree_type(self, typeStr, fromTheme='default', sub='tree'):
        
        R_THEMES = dict()
        R_THEMES['default'] = dict()
        R_THEMES['default']['tree'] = dict()
        R_THEMES['default']['tree']['types'] = dict()
        R_THEMES['default']['tree']['types']['Root'] = dict()
        R_THEMES['default']['tree']['types']['Root']['tagName'] = "R"
        R_THEMES['default']['tree']['types']['Root']['tagBg'] = "#DDB3B3"
        R_THEMES['default']['tree']['types']['Table']['tagName'] = "T"
        R_THEMES['default']['tree']['types']['Table']['tagBg'] = "#F0CFCF"
        R_THEMES['default']['tree']['types']['Dir']['tagName'] = "d"
        R_THEMES['default']['tree']['types']['Dir']['tagBg'] = "#F0CFCF"
        R_THEMES['default']['tree']['types']['File']['tagName'] = "f"
        R_THEMES['default']['tree']['types']['File']['tagBg'] = "#F8F8F8"
        R_THEMES['default']['tree']['types']['Text']['tagName'] = "t"
        R_THEMES['default']['tree']['types']['Text']['tagBg'] = "#F8F8F8"
        R_THEMES['default']['tree']['types']['Var']['tagName'] = "v"
        R_THEMES['default']['tree']['types']['Var']['tagBg'] = "#9EEEEB"
        R_THEMES['default']['tree']['types']['Image']['tagName'] = "i"
        R_THEMES['default']['tree']['types']['Image']['tagBg'] = "#A5E0F5"
        R_THEMES['default']['tree']['types']['Bytes']['tagName'] = "b"
        R_THEMES['default']['tree']['types']['Bytes']['tagBg'] = "#E2E389"
        R_THEMES['default']['tree']['types']['Code']['tagName'] = "c"
        R_THEMES['default']['tree']['types']['Code']['tagBg'] = "#F8F8F8"
        R_THEMES['default']['tree']['types']['None']['tagName'] = "n"
        R_THEMES['default']['tree']['types']['None']['tagBg'] = "#FFFFFF"
        
        # R_THEMES['default']['tree']['types']['Root']['tagName'] = "R"
        # R_THEMES['default']['tree']['types']['Root']['tagBg'] = "#DDB3B3"
        
        if useTheme not in R_THEMES.keys():
            print("Theme '{}' does not exist.".format(useTheme))
            return None
        theme = R_THEMES[useTheme]
        if sub not in theme.keys():
            print("Theme ['{}'] ['{}'] does not exist.".format(useTheme, sub))
            return None
        sub = theme[sub]
        if 'types' not in sub.keys():
            print("Theme ['{}']['{}']['{}'] does not exist.".format(useTheme, sub, 'types'))
            return None
        types = sub['types']
        if typeStr in types.keys():
            return types[typeStr]
        print("Theme ['{}']['{}']['{}']['{}'] does not exist.".format(useTheme, sub, 'types', typeStr))
        return None

    # Binding callback functions
    def on_selectItem(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

        if self.tree.selection() is (): # if empty select 'root'
            self.tree.focus('root')
            self.tree.selection_set('root')
            return
        self.selected_items = self.tree.selection() # tuple
        # print('Selected items:', self.selected_items)
        self.selected_data = {}
        for selected_uid in self.selected_items: # for multi selections
            self.selected_item_data = self.tree.item(selected_uid) # dict of data
            # print ('Selected row_text: {}'.format(self.selected_item_data['text']))
            self.selected_data[selected_uid] = self.selected_item_data # at key and data to dict
        print('Selected_data: {}'.format(self.selected_data))
            
        self.col = self.tree.identify_column(event.x)
        if self.col == '':
            self.col = '#0'
        if self.col == '#0':
            self.cell_value = self.selected_item_data['text']
        elif self.col == '#1':
            self.cell_value = self.selected_item_data['values'][0]
        elif self.col == '#2':
            self.cell_value = self.selected_item_data['values'][1]
        elif self.col == '#3':
            self.cell_value = self.selected_item_data['values'][2]
            
        print ("Selected_items: {}, col: '{}', cell_value: '{}'".format(self.selected_items, 
                                                            self.col, self.cell_value))

    def on_openSelected(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, sys._getframe().f_code.co_name, 
                                "self, {}".format(str(event))))

        self.selected_items = self.tree.selection()
        # print('Selected items:', self.selected_items)
        self.selected_data = {}
        for selected_uid in self.selected_items:
            self.selected_item_data = self.tree.item(selected_uid) # dict of data
            # print ('Selected row_text: {}'.format(self.selected_item_data['text']))
            self.selected_data[selected_uid] = self.selected_item_data # at key and data to dict
        print('Selected_data: {}'.format(self.selected_data))
            
    def on_showContexMenu(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_doContexMenu(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    # Utility functions
    def new_uid(self):
        uid = uuid.uuid4() 
        print ("The new id is : '{}'".format(uid)) 
        return uid
    
    def node_exists(self, nodeUID):
        return nodeUID in B.nodes
    
    def get_node(self, nodeUID):
        return B.nodes[nodeUID]
    
    # Use this on leaf nodes only.
    # Do NOT use this on Table nodes as it will disassociate all child nodes
    # Use alter_table_node_uid(oldUID, newUID) instead
    def alter_leaf_node_uid(self, oldUID, newUID=None):
        if newUID is None:
            newUID = self.newUID()
        oldNode = B.nodes[oldUID]
        oldNode['uid'] = newUID # Change the internal 'uid' ref as well
        B.nodes[newUID] = oldNode
        del B.nodes[oldUID]
        return newUID
    
    # Use this on Table nodes. It will reassociate all child nodes
    def alter_table_node_uid(self, oldUID, newUID=None):
        pass
    
    def ask_open_startup(self, initdir='./'):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            'self'))
        startup =  filedialog.askopenfilename(
            initialdir = initdir, 
            title = "Select startup file to use", 
            filetypes = (("json files","*.json|*.JSON"), 
                        ("sqlite files","*.sqlite*"), 
                        ("all files","*.*")))
        # self.use_startup = startup
        print("Selected startup: '{}'".format(startup))
        return startup

    def ask_open_root(self, initdir='./'):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            'self'))
        newroot =  filedialog.askopenfilename(
            initialdir = initdir, 
            title = "Select root file to use", 
            filetypes = (("json files","*.json|*.JSON"), 
                        ("sqlite files","*.sqlite*"), 
                        ("all files","*.*")))
        # self.use_startup = startup
        print("Selected root: '{}'".format(newroot))
        return newroot

    def save_root_as(self):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            'self'))
        if B.flDirtyRoot:
            if ask_yes_no('Save changes before making a copy?', 
                            'Save changes before copying?'):
                pass # # TODO: def save_root(): # #
        rootpath = _self.ask_save_root_as()
        if rootpath is None:
            return False
        with rootpath as newroot:
            # save a copy of current root and prefs
            # Build the nodes and prefs into one dict object
            newRootData = {}
            newRootData[B.N_KEY] = B.nodes
            newRootData[B.P_KEY] = B.prefs
            # Or can I just use B.TREEROOT
            
            print("Saving copy of root to: '{}'".format(rootpath))
            json.dump(newRootData, outfile, sort_keys=False, 
                        ensure_ascii=True, indent=2)
            B.flDirtyRoot = False
        return True
    
    def _ask_save_root_as(self, initdir='./', initfile='root.json', mode='w'):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            'self'))
        saverootas =  filedialog.asksaveasfilename(
            initialdir = initdir, 
            title = "Select file to save root to", 
            defaultext = initfile,
            mode = "w",
            filetypes = (("json files", "*.json|*.JSON"), 
                        ("all files","*.*")))
        # self.use_startup = startup
        print("Opened selected root: '{}'".format(saveroot))
        return saverootas

    def ask_yes_no(self, winMessage='', winTitle='Question...'):
        result = messagebox.askyesno(
                message=winMessage,
                icon='question', title=winTitle)
        return result # returns True or False

    def ask_ok_cancel(self, winMessage='', winTitle='Question...'):
        result = messagebox.askokcancel(
                message=winMessage,
                icon='question', title=winTitle)
        return result # returns True or False

    def show_info(self, winMessage='', winTitle='For your information...'):
        result = messagebox.showinfo(
                message=winMessage,
                icon='info', title=winTitle)
        return

    def show_warning(self, winMessage='', winTitle='Warning...'):
        result = messagebox.showwarning(
                message=winMessage,
                icon='warning', title=winTitle)
        return

    def show_error(self, winMessage='', winTitle='Error...'):
        result = messagebox.showerror(
                message=winMessage,
                icon='error', title=winTitle)
        return

    def getColor(self, returnType='hex'):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, '{}'".format(returnType)))
        # where the first item of the tuple gives the RGB values, 
        # while the second item of the tuple gives the hexadecimal color code.

        rgbcolor, hexcolor = askcolor(initial='red', parent=parentWin, alpha=False)
        # ((99, 222, 170), ‘#63deaa’) or (None, None)
        if hexcolor is None: # if user canceled
            print('User cancelled')
            return None
        if returnType.lower() != 'rgb':
            print('Colour chosen: {}'.format(hexcolor))
            return hexcolor # return Hex str value
        print('Colour chosen: {}'.format(rgbcolor))
        return rgbcolor # return RGB tuple
    
    def ask_string(self, title, request, parentObj):
        print('{}: {}({})'.format(self.__class__.__name__, 
                    sys._getframe().f_code.co_name, 
                    "self, '{}', '{}', {}".format(title, request, parentObj)))
        answer = simpledialog.askstring(title, request, parent=parentObj)
        if answer is not None:
            print("Answered: '{}'".format(answer))
            return answer
        print("User cancelled")
        return answer
    
    def ask_integer(self, title, request, parentObj, Min=-1000000, Max=1000000):
        print('{}: {}({})'.format(self.__class__.__name__, 
                    sys._getframe().f_code.co_name, 
                    "self, '{}', '{}', {}".format(title, request, 
                                        parentObj, Min, Max)))
        answer = simpledialog.askinteger(title, request, parent=parentObj, 
                                        minvalue=Min, maxvalue=Max)
        if answer is not None:
            print("Answered: '{}'".format(answer))
            return answer
        print("User cancelled")
        return answer
    
    def ask_float(self, title, request, parentObj, Min=-0.0000001, Max=1000000.0):
        print('{}: {}({})'.format(self.__class__.__name__, 
                    sys._getframe().f_code.co_name, 
                    "self, '{}', '{}', {}".format(title, request, 
                                        parentObj, Min, Max)))
        answer = simpledialog.askfloat(title, request, parent=parentObj, 
                                        minvalue=Min, maxvalue=Max)
        if answer is not None:
            print("Answered: '{}'".format(answer))
            return answer
        print("User cancelled")
        return answer
    
    def tuple2list(self, tup):
        mylist = []
        for x in tup:
            mylist.append(x)
        return mylist

    def list_union(self, list1, list2):
        # Returns a sorted list from the union of 2 list without duplicates
        union_list = list(set.union(set(list1), set(list2)))
        union_list.sort()
        # print('Union list: {}'.format(union_list))
        return union_list

    def list_intersection(self, list1, list2):
        set1 = set(list1)
        set2 = set(list2)
        my_intersection = set1.intersection(set2)
        intersection_list = list(my_intersection)
        intersection_list.sort()
        #print('Intersection of lists: {}'.format(intersection_list))
        return intersection_list

    def find_pref(self, prefName, reqType=None):
        print("{}: {}({})".format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, '{}', '{}'".format(prefName, reqType)))
        
        searchplaces = [B.prefs, B.PREFS]
        
        for searchplace in searchplaces:
            if prefName in searchplace.keys():
                # print('"{}" was found with value {}'.format(prefName, searchplace[prefName]))
                return searchplace[prefName]

        print('"{}" was not found anywhere'.format(prefName))
        return

    def get_pref(self, prefName, reqType=None):
        print('Called get_pref({}, {})'.format(prefName, reqType))
        
        if prefName in B.prefs.keys():
            return B.prefs[prefname]
        print('"{}" does not exist in prefs'.format(prefName))
        return

    def get_PREF(self, prefName, reqType=None):
        print('Called get_pref({}, {})'.format(prefName, reqType))
        
        if prefName in B.PREFS.keys():
            return B.PREFS[prefname]
        print('"{}" does not exist in PREFS'.format(prefName))
        return

    def set_pref(self, prefname, prefvalue):
        print('Called: set_pref({}, {})'.format(prefname, prefvalue))
        B.prefs[prefname] = prefvalue
        return True

    def set_PREF(self, prefname, prefvalue):
        print('Called: set_pref({}, {})'.format(prefname, prefvalue))
        B.PREFS[prefname] = prefvalue
        return True

    def disable_menu_item(self, menu_obj, menu_index):
        menu_obj.entryconfigure(menu_index, state='disabled')
        #print('Disabled menu item:', menu_index)

    def enable_menu_item(self, menu_obj, menu_index):
        menu_obj.entryconfigure(menu_index, state='normal')
        #print('Enabled menu item:', menu_index)

    def toggle_menu_item(self, menu_obj, menu_index):
        menu_state = menu_obj.entrycget(menu_index, 'state')
        if menu_state == tk.DISABLED or menu_state == 'disabled':
            self.enable_menu_item(menu_obj, menu_index)
        else:
            self.disable_menu_item(menu_obj, menu_index)

    def merge_dict_of_dicts(self, x, y):
        z = {}
        overlapping_keys = x.keys() & y.keys()
        for key in overlapping_keys:
            z[key] = dict_of_dicts_merge(x[key], y[key])
        for key in x.keys() - overlapping_keys:
            z[key] = deepcopy(x[key])
        for key in y.keys() - overlapping_keys:
            z[key] = deepcopy(y[key])
        return z

    def merge_dicts(self, x, y):
        z = {**x, **y}
        return z

    def unDotMap(self, dotMappedDict):
        return dotMappedDict.toDict()
        '''python
d = {'a':1, 'b':2}

m = DotMap(d)
print(m)
# DotMap(a=1, b=2)

print(m.toDict())
# {'a': 1, 'b': 2}
'''

    def first_word(self, sentence):
        sentence = sentence.split()[0]
        s = ''.join(word[0].upper() + word[1:] for word in sentence.split())
        return s

    def wordcase(self, sentence):
        s = ' '.join(word[0].upper() + word[1:] for word in sentence.split())
        return s

    def sentence_case(self, sentence):
        s = ''.join(sentence[0].upper() + sentence[1:])
        return s

    # File menu callback functions
    def on_file_new_root(self, FILE=None, TYPE=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, '{}', '{}'".format(FILE, TYPE)))

    def on_file_open_root(self, FILE='root.json', TYPE='json'):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, '{}', '{}'".format(FILE, TYPE)))

    def on_file_save_root(self, FILE='root.json', TYPE='json'):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, '{}', '{}'".format(FILE, TYPE)))

        # The root must contain both the default B.nodes and B.prefs.
        newRootData = {}
        newRootData[B.N_KEY] = B.nodes
        newRootData[B.P_KEY] = B.prefs
        
        # Save data to root.json file
        if TYPE == 'json':
            with open(FILE, 'w') as outfile:
                print("Writing default node prefs to: '{}'".format(FILE))
                json.dump(newRootData, outfile, sort_keys=False, ensure_ascii=True, indent=2)
        else:
            print('Unsupported Root file type.')

    def on_file_save_root_copy(self, FILE='root.json', TYPE='json'):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, '{}', '{}'".format(FILE, TYPE)))

        # The root must contain both the default nodes and prefs.
        newRootData = {}
        newRootData[B.N_KEY] = B.nodes
        newRootData[B.P_KEY] = B.prefs
        
        # Save data to root.json file
        if TYPE == 'json':
            with open(FILE, 'w') as outfile:
                print("Writing new root to: '{}'".format(FILE))
                json.dump(newRootData, outfile, sort_keys=False, ensure_ascii=True, indent=2)
        else:
            print('Unsupported Root file type.')
            
    def on_file_save_prefs(self, FILE='root.json', TYPE='json'):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, '{}', '{}'".format(FILE, TYPE)))

        # The root must contain both the default nodes and prefs.
        newRootData = {}
        newRootData[B.N_KEY] = B.nodes
        newRootData[B.P_KEY] = B.prefs
        
        # Save data to root.json file
        if TYPE == 'json':
            with open(FILE, 'w') as outfile:
                print("Saving root prefs to: '{}'".format(FILE))
                json.dump(newRootData, outfile, sort_keys=False, ensure_ascii=True, indent=2)
        else:
            print('Unsupported Root file type.')

    def on_file_save_root_as(self, FILE='root.json', TYPE='json'):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, '{}', '{}'".format(FILE, TYPE)))
        
    def on_file_backup_root(self, FILE='root.json', TYPE='json'):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, '{}', '{}'".format(FILE, TYPE)))

    def on_window_close(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))
        if B.flDirtyRoot is True:
            if prefs['flAutoSaveOnClose'] is False:
                if tkMessageBox.askokcancel("Save", "Save before closing?"):
                    self.root.destroy()
                else:
                    return # User cancelled so don't do anything
            else: # Auto save is on
                self.on_file_save_root() # save root before closing
                self.root.destroy()
        self.root.destroy() # Root is not dirty

    def on_file_close_root(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_file_quit(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))
        self.root.destroy()
        sys.exit(0)

    # Edit menu callback functions
    def on_tree_copy(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_tree_paste(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_tree_cut(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_tree_delete(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_edit_root_prefs(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_edit_startup_prefs(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    # New menu callback functions
    def on_new_table(self):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_new_text(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_new_outline(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_new_code(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_new_image(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_new_undefined(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_new_string(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_new_integer(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_new_float(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_new_boolean(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_new_dict(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_new_list(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_new_tuple(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_new_set(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_new_path(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_new_address(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_new_none(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    # View menu callback functions
    def on_view_show_info(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    # Dynamic user menu callback functions
    def on_user_add_bookmark(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_user_bookmarks(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    # Help menu callback functions
    def on_help_about(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    def on_help_online_help(self, event=None):
        print('{}: {}({})'.format(self.__class__.__name__, 
                            sys._getframe().f_code.co_name, 
                            "self, {}".format(str(event))))

    # These are unused functions
    def unused(self):
        # Load node prefs from last root file
        def get_node_prefs(self, FILE="./root.json", TYPE="json", KEY='prefs'):
            print("{}: {}({})".format(self.__class__.__name__, 
                                sys._getframe().f_code.co_name, 
                                "self, '{}', '{}', '{}'".format(FILE, TYPE, KEY)))
                                
            if not os.path.isfile(FILE): # Check again with default values
                print("Can't find the default root file: {}...".format(FILE))
                # **** TO-DO **** #
                # Show askOpenFileDialog()
                print('Creating the default root file named: {}'.format(B.R_DEFAULT))
            
                # ** TO DO ** save default nodes to FILE as well
                # the root must contain both the default node prefs and default nodes.
                data = dict()
                data[B.N_KEY] = B.R_DEFAULT_NODES
                data[B.P_KEY] = B.prefs
                
                # Save data to root.json file
                if TYPE == 'json':
                    with open(FILE, 'w') as outfile:
                        print('Writing default node prefs to: {}'.format(FILE))
                        json.dump(data, outfile, sort_keys=false, ensure_ascii=True, indent=2)
                    
            # Open FILE and get node prefs
            with open(FILE) as json_file:
                treeroot = json.load(json_file)
                B.prefs = treeroot[KEY]
                
                # merge default prefs with treeroot prefs
                #prefs = self.merge_dicts(prefs, treeroot['prefs'])
                            
                if 'fileFormat' not in B.prefs: # format 1.0 did not have a fileFormat key
                    B.prefs['fileFormat'] = 1.0 # create 'fileFormat' key with value 1.0
                if B.prefs['fileFormat'] == 1.0:
                    print('Updating root nodes from version 1.0 to 1.1', '\n')
                    
                    treenodes = treeroot[B.N_KEY]
                    B.nodes = {}
                    for x in range(0, len(treenodes)):
                        node = treenodes[x]
                        uid = node[B._T_UID]
                        B.nodes[uid] = node
                    prefs['fileFormat'] = 1.1 # node format version is now 1.1
                    treeroot[N_KEY] = B.nodes
                    treeroot[P_KEY] = B.prefs
                    #B.nodes = B.nodes

                    # Save updated treeroot with prefs
                    with open(filename, 'w') as outfile:
                        print('Saving updated version of {}\n'.format(filename))
                        json.dump(treeroot, outfile, sort_keys=False, ensure_ascii=True, indent=2)
                    # print('Upgraded fileFormat to 1.1 format')

            # Read in prefs
            #print('Reading node prefs from: {}'.format(FILE))
            with open(FILE) as prefs_file: # Open for Reading
                treeroot = json.load(prefs_file) # Store prefs dict
                #print('Pre-merge prefs', prefs)
                if KEY is not None: # Get data using dict key 
                    # merge default prefs with treeroot prefs
                    B.prefs = self.merge_dicts(B.prefs, treeroot[KEY])
                else:
                    B.prefs = self.merge_dicts(B.prefs, treeroot)
                #print('Post-merge prefs', B.prefs)

        def get_nodes(self, FILE='./root.json', TYPE='json', KEY='nodes'):
            print("{}: {}({})".format(self.__class__.__name__, 
                                sys._getframe().f_code.co_name, 
                                "self, '{}', '{}', '{}'".format(FILE, TYPE, KEY)))

            with open(FILE) as json_file:
                B.TREEROOT = json.load(json_file)
                
                # nodes is where we get and set all node changes
                B.R_NODES = B.nodes = B.TREEROOT[KEY]

        # Mutable on startup (S_) (Can be appended too)
        # ~ S_ITEMS_LIST = ["autoSaveInterval", "backupExt", "backupDirName", "dataDirName",
            # ~ "dataDirName", "dataStoreType", "dataStoreName", "dataKey", "flAutoSave", 
            # ~ "flAutoSaveOnChange", "flAutoSaveOnClose", "flEnableAgents", "flEnableWebServer", 
            # ~ "flErrorLogs", "flFirstStartup", "flNightlyBackups", "flWebErrorLogs", "flWebLogs", 
            # ~ "flWebStats", "lastBackupCount", "lastBackupName", "lastBackupDate", "lastRoot", 
            # ~ "lastRootPath", "lastRootType", "logDirName", "nodeKey", "openBrowserCommand", 
            # ~ "prefsKey", "recentRoots", "webCGIext", "webHomePage", "webServerHostName", 
            # ~ "WebServerPorts", "WebSiteDirName"]

def main(argv):
    import argparse
    from argparse import RawDescriptionHelpFormatter
    import textwrap

    # help flag provides flag help
    # store_true actions stores argument as True

    parser = argparse.ArgumentParser( prog='Pysist', 
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            What is %(prog)s?
            --------------------------------
                %(prog)s is a visual persistent variable and file saving 
                system with editing and manipulation of all data contained 
                or imported into it.
                %(prog)s is NOT another Python IDE, nor will it ever be. 
                There are so many well established IDEs out there already. 
                To that end, %(prog)s opens all contained files with whatever 
                your default editor is for that type of file. 
                So you can have the best of both worlds.
            '''), epilog=textwrap.dedent('''\
            Thank you for taking the time to play with %(prog)s.
            -----------------------------------------------
            PS. I was going to name this program 'Pyist'...
                but thought better of it.
            -----------------------------------------------
                                                          .
            '''))
    
    parser.add_argument('-v', '--version', action='version', 
        version='This is %(prog)s version 0.0.1', 
        help="Show the version of %(prog)s")

    parser.add_argument('-d', '--debug', action='store_true', default=False, 
        help="Forces debug mode. Gives more processing feed-back at run-time.")

    parser.add_argument('-t', '--test', action='store_true', default=False, 
        help="Forces testing mode. Uses a copy of the default root and sqlite storage.")

    parser.add_argument('-w', '--window', action='store_true', default=False, 
        help="Use -w to open %(prog)s as a windowless class. Default is False")

    parser.add_argument('-s', '--startup', type=str, 
        help="Re-defines the startup file to load. Enables the testing of different startup files.")

    parser.add_argument('-r', '--root', type=str, 
        help="Re-defines the root file to open. Enables the testing of new root files.")

    args = parser.parse_args()

    root = tk.Tk()
    app=Window(root, args)
    root.mainloop() 

if __name__ == "__main__":
   main(sys.argv[1:])
