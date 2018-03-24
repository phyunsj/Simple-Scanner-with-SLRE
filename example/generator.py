#!/usr/bin/env python

from string import Template
import sys, pprint, os
import re
import json
import time
import shutil

# Add the directory containing your module to the Python path
scriptpath = "./scannerTypes.py"
sys.path.append(os.path.abspath(scriptpath))
from scannerTypes import *

scriptpath = "./scannerMethods.py"
sys.path.append(os.path.abspath(scriptpath))
from scannerMethods import *

# Make a separate generator for all differnt target for easy maintenance & simplicity even though  database.xlsx is beging read multiple times. 
if __name__ == '__main__':

    types = scannerTypes()
    types.codegen( )

    methods = scannerMethods()
    methods.codegen()
    methods.close()
