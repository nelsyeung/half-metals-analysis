#!/usr/bin/env python3
""" Main python program for running codes """
import os
import sys
import inspect

# Add extra libraries' directories to import list
baseLibDir = os.path.join(os.path.realpath(os.path.dirname(
    inspect.getfile(inspect.currentframe()))), 'nlib')
compoundsLibDir = os.path.join(baseLibDir, 'compounds')

sys.path.append(compoundsLibDir)

# Import own libraries
from five_elements import FiveElements

if __name__ == '__main__':
    compounds = FiveElements('CFMGS/B2', 'Co Fe Mn Ga Si',
                             'sc_5_elements_b2', '5.333751602764')
    compounds.generateConcentrations(20)