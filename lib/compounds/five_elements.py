""" Class for generate 5 elements compounds """
import os
import sys
import inspect

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

    def generateConcentrations(self, num, **kwargs):
        """ Generate the required permutations of concentrations """
        if self.potFile == 'sc_5_elements_b2':
            a, b, c, d, e = 1.0, 0.5, 0.0, 0.5, 0.0
            step = b / (num - 1)
            precision = len(str(step).split('.')[1])
            conc = [None]*5
            conc[0] = nmod.float2str(precision, a)
            
            for i in range(0, num * num):
                x, y = i % num, int(i / num)
                conc[1] = nmod.float2str(precision, b - x * step)
                conc[2] = nmod.float2str(precision, c + x * step)
                conc[3] = nmod.float2str(precision, d - y * step)
                conc[4] = nmod.float2str(precision, e + y * step)
                self.create(conc[0] + '_' + conc[1] + '_' + conc[2]
                            + '_' + conc[3] + '_' + conc[4], **kwargs)
        elif self.potFile == 'fcc_5_elements_l21':
            a, b, c, d, e = 1.0, 1.0, 0.0, 1.0, 0.0
            step = b / (num - 1)
            precision = len(str(step).split('.')[1])
            conc = [None]*5
            conc[0] = nmod.float2str(precision, a)
            
            for i in range(0, num * num):
                x, y = i % num, int(i / num)
                conc[1] = nmod.float2str(precision, b - x * step)
                conc[2] = nmod.float2str(precision, c + x * step)
                conc[3] = nmod.float2str(precision, d - y * step)
                conc[4] = nmod.float2str(precision, e + y * step)
                self.create(conc[0] + '_' + conc[1] + '_' + conc[2]
                            + '_' + conc[3] + '_' + conc[4], **kwargs)
        else:
            print(self.potFile + ' has not yet been implemented.')
            nmod.nexit()
