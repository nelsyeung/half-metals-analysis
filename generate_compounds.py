#!/usr/bin/env python3
""" Main python program for running codes """
import os
import sys
import inspect

# Add extra libraries' directories to import list
baseLibDir = os.path.join(os.path.realpath(os.path.dirname(
    inspect.getfile(inspect.currentframe()))), 'lib')
compoundsLibDir = os.path.join(baseLibDir, 'compounds')
analysisLibDir = os.path.join(baseLibDir, 'analysis')

sys.path.append(compoundsLibDir)
sys.path.append(analysisLibDir)

# Import own libraries
from five_elements import FiveElements
from analysis import Analysis

if __name__ == '__main__':
    compounds = FiveElements('CFMGS/B2', 'Co Fe Mn Ga Si',
                            'sc_5_elements_b2', '5.333751602764')
    # compounds.settings['nktab'] = '1000'
    # compounds.settings['SCF']['NE'] = '60'
    # compounds.settings['DOS']['NE'] = '100'
    # compounds.settings['BSF']['NK'] = '120'
    compounds.generateConcentrations(21)
    compounds.generateDOS()
    compounds.generateBSF()
