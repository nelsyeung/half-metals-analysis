#!/usr/bin/env python
""" Generate compounds """
import os
import sys
import inspect

# Add extra libraries' directories to import list
baseLibDir = os.path.join(os.path.realpath(os.path.dirname(
    inspect.getfile(inspect.currentframe()))), 'lib')
compoundsLibDir = os.path.join(baseLibDir, 'compounds')

sys.path.append(compoundsLibDir)

# Import own libraries
from five_elements import FiveElements

if __name__ == '__main__':
    nktab = 250
    compounds = FiveElements('CFMGS/B2', 'Co Fe Mn Ga Si',
                            'sc_5_elements_b2', '5.333751602764')
    compounds.generateConcentrations(21, mode='SP-SREL', nktab=nktab, NE=30)
    compounds.generateDOS(mode='SP-SREL', nktab=nktab, NE=50,
                          EMIN=0.74, EMAX=1.0, ImE=0.0005)
    compounds.generateBSF(nktab=nktab)
