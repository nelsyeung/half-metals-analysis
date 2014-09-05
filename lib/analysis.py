""" Base analysis class for analysing DOS and BLOCHSF data """
import os
import sys
import inspect
import math
from scipy import integrate

# Add extra libraries' directories to import list
baseLibDir = os.path.join(os.path.realpath(os.path.dirname(
             inspect.getfile(inspect.currentframe()))), '..')
sys.path.append(baseLibDir)

# Import own libraries
import nmod

class Analysis(object):
    """ Analysis base class """
    def __init__(self, mainDir):
        baseDir = os.path.join(os.path.dirname(os.path.realpath(
            inspect.getfile(inspect.currentframe()))), '..')
        self.mainDir = os.path.join(baseDir, mainDir)
        self.rawDir = os.path.join(self.mainDir, 'raw')
        self.analysisDir = os.path.join(self.mainDir, 'analysis')
        error = False
        
        # Check if the required directories exist
        if os.path.isdir(self.mainDir) is False:
            print('The directory provided does not exists.')
            error = True

        if os.path.isdir(self.rawDir) is False:
            print('The directory provided does have a raw folder.')
            error = True
        else:
            # Check if there are any data in the raw folder.
            os.chdir(self.rawDir)

            numData = len([name for name in os.listdir('./')
                          if os.path.isdir(name)])

            if numData == 0:
                print('No data in ' + os.path.join(mainDir, 'data') + '.')
                print('Please make sure that your data are in that folder.')
                error = True

        if error:
            nmod.nexit()
        else:
            os.chdir(self.rawDir)

    def bandGap(self, aInit, stripSize, stepSize):
        """ Band gap analysis """
        iterations = int(math.fabs(aInit) / stepSize) + 1
        concentrations = []
        I_bg = []
        normalised = []
        outFile = os.path.join(self.analysisDir, 'band_gap.txt')
        normalisedFile = os.path.join(self.analysisDir,
                                      'band_gap_normalised.txt')

        # Check if the band gap analysis file already exists,
        # if it exists, then remove it.
        if os.path.isfile(outFile) is True:
            os.remove(outFile)
        if os.path.isfile(normalisedFile) is True:
            os.remove(normalisedFile)
        
        for _, dirs, _ in os.walk('./'):
            for dirname in dirs:
                dos = nmod.getDOS(os.path.join(self.rawDir,
                    dirname, 'dos.agr'), 'down')
                dosInterp = nmod.getInterp1d(dos)
                integrals = []

                for i in range(iterations):
                    delta = i * stepSize
                    a = aInit + delta 
                    b = aInit + stripSize + delta
                    integral = integrate.quad(dosInterp, a, b)[0]
                    integrals.append(integral)

                I_bg.append(min(integrals))
                concentrations.append(dirname)

                with open(outFile, 'a+') as f:
                    f.write(dirname + ' ' + str(min(integrals)) + '\n')

        # Normalise the integrals and store as a new file.
        normalised = nmod.normalise(I_bg)
        with open(normalisedFile, 'a+') as f:
            for i in range(len(normalised)):
                f.write(concentrations[i] + ' ' + str(normalised[i]) + '\n')
