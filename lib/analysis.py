""" Base analysis class for analysing DOS and BLOCHSF data """
import os
import sys
import inspect

# Add extra libraries' directories to import list
baseLibDir = os.path.join(os.path.realpath(os.path.dirname(
             inspect.getfile(inspect.currentframe()))), '..')
sys.path.append(baseLibDir)

# Import own libraries
import nmod

class Analysis(object):
    """ Analysis base class """
    def __init__(self, dataDir):
        baseDir = os.path.join(os.path.dirname(os.path.realpath(
            inspect.getfile(inspect.currentframe()))), '..', '..')
        self.dataDir = os.path.join(baseDir, dataDir, 'data')
