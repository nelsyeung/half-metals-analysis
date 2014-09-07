#!/usr/bin/env python
""" Analyse data """
import os
import sys
import inspect

# Add extra libraries' directories to import list
baseLibDir = os.path.join(os.path.realpath(os.path.dirname(
    inspect.getfile(inspect.currentframe()))), 'lib')

sys.path.append(baseLibDir)

# Import own libraries
from analysis import Analysis

if __name__ == '__main__':
    analysis = Analysis('CFMGS/B2')
    # analysis.bandGap(-0.5, 0.4, 0.05)
    analysis.dosDiff(0.8)
