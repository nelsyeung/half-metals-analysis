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
    nktab = 1000
    compounds = FiveElements('CFMGS/L21', 'Co Fe Mn Ga Si',
                            'fcc_5_elements_l21', '10.6675032055')
    compounds.generateConcentrations(21, mode='SP-SREL', nktab=nktab, NE=60)
    compounds.generateDOS(mode='SP-SREL', nktab=nktab, NE=100,
                          EMIN=0.73, EMAX=1.0, ImE=0.0005)
    compounds.generateBSF(nktab=nktab, NK1=180, NK2=180,
                          EMIN=0.8652, EMAX=0.8652)
    # compounds.generateBSF(nktab=nktab, NK1=180, NK2=180,
    #                       EMIN=0.8652, EMAX=0.8652, iterations=10)
