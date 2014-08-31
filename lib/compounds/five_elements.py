""" Class for generate 5 elements compounds """
import os
import sys
import inspect
import math

baseLibDir = os.path.join(os.path.realpath(os.path.dirname(
             inspect.getfile(inspect.currentframe()))), '..')
sys.path.append(baseLibDir)
import nmod
from compound import Compound

class FiveElements(Compound):
    """ Five elements compound child class """
    def __init__(self, jobsDir, elements, potFile, alat):
        numElements = len(elements.split())

        if numElements != 5:
            print('Expecting 5 elements, but ' + numElements
                  + ' (' + elements + ') were inputted.')
            nmod.nexit()

        Compound.__init__(self, jobsDir, elements, potFile, alat)

    def generateConcentrations(self, num):
        """ Generate the required permutations of concentrations """
        if self.potFile == 'sc_5_elements_b2':
            a, b, c, d, e = 1.0, 0.5, 0.0, 0.5, 0.0
            step = b / (num - 1)
            precision = len(str(step).split('.')[1])
            conc1 = nmod.float2str(precision, a)
            
            for i in range(0, num * num):
                x, y = i % num, int(i / num)
                conc2 = nmod.float2str(precision, b - x * step)
                conc3 = nmod.float2str(precision, c + x * step)
                conc4 = nmod.float2str(precision, d - y * step)
                conc5 = nmod.float2str(precision, e + y * step)
                self.create(conc1 + '_' + conc2 + '_'
                            + conc3 + '_' + conc4 + '_' + conc5)
        else:
            print(self.potFile + ' has not yet been implemented.')
            nmod.nexit()
