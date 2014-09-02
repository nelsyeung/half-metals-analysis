""" Class for analysing DOS and BLOCHSF data """
import os
import sys
import inspect

class Analysis(object):
    """ Analysis base class """
    def __init__(self, dataDir):
        baseDir = os.path.join(os.path.dirname(os.path.realpath(
            inspect.getfile(inspect.currentframe()))), '..', '..')
        self.dataDir = os.path.join(baseDir, dataDir, 'data')
