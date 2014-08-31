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

    def generateConcentrations(self, num):
        """ Generate the required permutations of concentrations """
        if self.potFile == 'sc_5_elements_b2':
            a, b, c, d, e = 1.0, 0.5, 0.0, 0.5, 0.0
            dInit, eInit = d, e
            step = b / num
            precision = len(str(step).split('.')[1])
            aStr = nmod.float2str(precision, a)

            for _ in range(0, num + 1):
                d, e = dInit, eInit

                for _ in range(0, num + 1):
                    bStr = nmod.float2str(precision, b)
                    cStr = nmod.float2str(precision, c)
                    dStr = nmod.float2str(precision, d)
                    eStr = nmod.float2str(precision, e)
                    conc = (aStr + '_' + bStr + '_' + cStr
                            + '_' + dStr + '_' + eStr)

                    d = round(d - step, 3)
                    e = round(e + step, 3)
                    self.create(conc)

                b = round(b - step, 3)
                c = round(c + step, 3)
        else:
            print(self.potFile + ' has not yet been implemented.')
            nmod.nexit()
