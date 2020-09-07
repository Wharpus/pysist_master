#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  __init__.py
#  
#  2020 Flying Wharpus, Wharpus Ware <wharpus@gmail.com>
#  

import os
import importlib

path = os.path.dirname(os.path.abspath(__file__))
for m in os.listdir(path):
    if m.startswith("__"):
        continue
    module_name = ".{}".format(m.replace(".py", ''))
    module = importlib.import_module(module_name, "Pysist")
    globals().update(
        {n: getattr(module, n) for n in module.__all__} if hasattr(module, '__all__') 
        else 
        {k: v for (k, v) in module.__dict__.items() if not k.startswith('_')
    })
