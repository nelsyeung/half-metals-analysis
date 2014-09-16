""" Base analysis class for analysing DOS and BLOCHSF data """
import os
import sys
import inspect
import math
import time
from operator import itemgetter
from scipy import integrate
from scipy.optimize import curve_fit

# Add extra libraries' directories to import list
baseLibDir = os.path.join(os.path.realpath(os.path.dirname(
             inspect.getfile(inspect.currentframe()))), '..')
sys.path.append(baseLibDir)

# Import own libraries
import nmod

def checkAnalysisFiles(outFile, normalisedFile):
    """
    Check if the analysis file already exists,
    if it does, then remove it.
    """
    if os.path.isfile(outFile) is True:
        os.remove(outFile)

    if os.path.isfile(normalisedFile) is True:
        os.remove(normalisedFile)

def getDOS(dosFile, rawFile, spin):
    """
    Get DOS data from either the data folder or the raw folder.
    It's faster if the data is in the data folder,
    where it's supposed to be processed.
    """
    dos = []

    if os.path.isfile(dosFile):
        with open(dosFile) as f:
            for l in f:
                line = l.rstrip()
                x = float(line.split()[0])
                y = float(line.split()[1])
                dos.append([x, y])
    else:
        dos = nmod.getDOS(rawFile, spin)

    return dos

def getBSF2D(bsfFile, rawFile, spin, numSites):
    """
    Get 2D BSF data from either the data folder or the raw folder.
    It's faster if the data is in the data folder,
    where it's supposed to be processed.
    """
    bsf = []

    if os.path.isfile(bsfFile):
        with open(bsfFile) as f:
            for l in f:
                line = l.rstrip()
                x = float(line.split()[0])
                y = float(line.split()[1])
                bsf.append([x, y])
    else:
        bsf = nmod.getBSF2D(rawFile, spin, numSites)

    return bsf

def lorentzian(x0, I):
    """ Lorentzian with 1 peak """
    return lambda x, y: (I * y*y) / ( (x - x0)*(x - x0) + y*y )

class Analysis(object):
    """ Analysis base class """
    def __init__(self, mainDir):
        baseDir = os.path.join(os.path.dirname(os.path.realpath(
            inspect.getfile(inspect.currentframe()))), '..')
        self.mainDir = os.path.join(baseDir, mainDir)
        self.rawDir = os.path.join(self.mainDir, 'raw')
        self.dataDir = os.path.join(self.mainDir, 'data')
        self.analysisDir = os.path.join(self.mainDir, 'analysis')
        self.listDataDir = []
        error = False
        
        # Check if the required directories exist
        if os.path.isdir(self.mainDir) is False:
            print('The directory provided does not exists.')
            error = True

        if (os.path.isdir(self.rawDir) is False
                and os.path.isdir(self.dataDir) is False):
            print('The directory provided does have a raw or data folder.')
            error = True
        else:
            # Check if there are any data in the raw folder.
            numTotal = 0

            if os.path.isdir(self.dataDir) is True:
                numData = len([dirname for dirname in os.listdir(self.dataDir)
                    if os.path.isdir(os.path.join(self.dataDir, dirname))])
                if numData != 0:
                    numTotal += numData
                    self.listDataDir = sorted(os.listdir(self.dataDir))

            if os.path.isdir(self.rawDir) is True:
                numRaw = len([dirname for dirname in os.listdir(self.rawDir)
                    if os.path.isdir(os.path.join(self.rawDir, dirname))])
                if numRaw != 0 and len(self.listDataDir) == 0:
                    numTotal += numRaw
                    self.listDataDir = sorted(os.listdir(self.dataDir))

            if numTotal == 0:
                print('No data in ' + os.path.join(mainDir, 'data'))
                print('or in ' + os.path.join(mainDir, 'raw') + ',')
                print('Make sure that your data are in one of those folders.')
                error = True 
        if error:
            nmod.nexit()
        else:
            os.chdir(self.mainDir)

    def bandGap(self, aInit, stripSize, stepSize):
        """ Band gap analysis """
        print('Running band gap analysis...')
        iterations = int(math.fabs(aInit) / stepSize) + 1
        concentrations = []
        I_bg = []
        normalised = []
        outFile = os.path.join(self.analysisDir, 'band_gap.txt')
        normalisedFile = os.path.join(self.analysisDir,
                                      'band_gap_normalised.txt')

        checkAnalysisFiles(outFile, normalisedFile)

        # Define time variables for calculating time left.
        numData = len(self.listDataDir)
        numDataLeft = numData
        startTime = time.time()
        prevTime = startTime
        eachTimeTaken = []
        
        # Start the analysis process.
        for dirname in self.listDataDir:
            # Get DOS data.
            dosFile = os.path.join(self.dataDir, dirname, 'dos_down.txt')
            rawFile = os.path.join(self.rawDir, dirname, 'dos.agr')
            dos = getDOS(dosFile, rawFile, 'down')

            # Linearly interpolate the DOS data.
            dosInterp = nmod.getInterp1d(dos)
            integrals = []

            # Calculate minimum integral by translating a fixed width strip.
            for i in range(iterations):
                delta = i * stepSize
                a = aInit + delta 
                b = aInit + stripSize + delta
                integral = integrate.quad(dosInterp, a, b, limit=100)[0]
                integrals.append(integral)

            minIntegral = min(integrals)
            I_bg.append(-minIntegral)
            concentrations.append(dirname)

            with open(outFile, 'a+') as f:
                f.write(dirname + ' ' + str(minIntegral) + '\n')

            # Calculate time left.
            eachTimeTaken.append(time.time() - prevTime)
            prevTime = time.time()
            numDataLeft -= 1
            sys.stdout.write('\r' + str(numDataLeft) + '/' + str(numData)
                             + ' - Time left: ' + nmod.seconds2str(
                             nmod.findMean(eachTimeTaken) * numDataLeft)
                             + '         ')
            sys.stdout.flush()

        # Normalise the data and store as a new file.
        normalised = nmod.normalise(I_bg)
        print('\nNormalising band gap data...')
        with open(normalisedFile, 'a+') as f:
            for i in range(len(normalised)):
                f.write(concentrations[i] + ' ' + str(normalised[i]) + '\n')

        print('Band gap analysis completed. Time taken: '
               + nmod.seconds2str(time.time() - startTime))

    def dosDiff(self, vincinity):
        """ Difference between spin up and down DOS """
        print('Running DOS difference analysis...')
        concentrations = []
        I_dos = []
        normalised = []
        outFile = os.path.join(self.analysisDir, 'dos_diff.txt')
        normalisedFile = os.path.join(self.analysisDir,
                                      'dos_diff_normalised.txt')

        checkAnalysisFiles(outFile, normalisedFile)

        # Define time variables for calculating time left.
        numData = len(self.listDataDir)
        numDataLeft = numData
        startTime = time.time()
        prevTime = startTime
        eachTimeTaken = []

        # Start the analysis process.
        for dirname in self.listDataDir:
            # Get DOS data.
            dosUpFile = os.path.join(self.dataDir, dirname, 'dos_up.txt')
            dosDownFile = os.path.join(self.dataDir, dirname, 'dos_down.txt')
            rawFile = os.path.join(self.rawDir, dirname, 'dos.agr')
            dosUp = getDOS(dosUpFile, rawFile, 'up')
            dosDown = getDOS(dosDownFile, rawFile, 'down')

            # Correction to the Fermi level from the DOS data.
            dataLen = len(dosDown)
            truncated = []

            for i in range(dataLen):
                if math.fabs(dosDown[i][0]) < vincinity:
                    truncated.append(dosDown[i])

            correction = sorted(truncated, key=itemgetter(1))[0][0]

            # Shift the whole dataset.
            # for i in range(dataLen):
            #     dosUp[i][0] += correction
            #     dosDown[i][0] += correction

            # Linearly interpolate the DOS data.
            dosUpInterp = nmod.getInterp1d(dosUp)
            dosDownInterp = nmod.getInterp1d(dosDown)

            # Calculate the difference between the DOS at E-E_f = 0eV.
            dosDiff = dosUpInterp(correction) - dosDownInterp(correction)
            # dosDiff = dosDownInterp(0)
            I_dos.append(dosDiff)
            concentrations.append(dirname)

            with open(outFile, 'a+') as f:
                f.write(dirname + ' ' + str(dosDiff) + '\n')

            # Calculate time left.
            eachTimeTaken.append(time.time() - prevTime)
            prevTime = time.time()
            numDataLeft -= 1
            sys.stdout.write('\r' + str(numDataLeft) + '/' + str(numData)
                             + ' - Time left: ' + nmod.seconds2str(
                             nmod.findMean(eachTimeTaken) * numDataLeft)
                             + '         ')
            sys.stdout.flush()

        # Normalise the data and store as a new file.
        normalised = nmod.normalise(I_dos)
        print('\nNormalising DOS difference data...')
        with open(normalisedFile, 'a+') as f:
            for i in range(len(normalised)):
                f.write(concentrations[i] + ' ' + str(normalised[i]) + '\n')

        print('DOS difference analysis completed. Time taken: '
               + nmod.seconds2str(time.time() - startTime))

    def fermiVelocity(self, dE):
        """ Fermi velocity analysis """
        print('Running Fermi velocity analysis...')
        concentrations = []
        I_vf = []
        normalised = []
        outFile = os.path.join(self.analysisDir, 'fermi_velocity.txt')
        normalisedFile = os.path.join(self.analysisDir,
                                      'fermi_velocity_normalised.txt')

        checkAnalysisFiles(outFile, normalisedFile)

        # Define time variables for calculating time left.
        numData = len(self.listDataDir)
        numDataLeft = numData
        startTime = time.time()
        prevTime = startTime
        eachTimeTaken = []

        # Start the analysis process.
        for dirname in self.listDataDir:
            # Get the first and last 2D BSF data.
            bsfDownFile = os.path.join(self.dataDir, dirname,
                                        '1_bsf2d_down.txt')
            rawFile = os.path.join(self.rawDir, dirname,
                                   dirname + '_1_BLOCHSF_spol.bsf')
            bsfDownStart = getBSF2D(bsfDownFile, rawFile, 'down', 5)

            bsfDownFile = os.path.join(self.dataDir, dirname,
                                        '10_bsf2d_down.txt')
            rawFile = os.path.join(self.rawDir, dirname,
                                   dirname + '_10_BLOCHSF_spol.bsf')
            bsfDownEnd = getBSF2D(bsfDownFile, rawFile, 'down', 5)

            # Get the ending position.
            # First crop half of the data, to remove the other peak.
            # Then get the position of the peak by finding the position of max.
            truncated = []
            for n in range(int(len(bsfDownEnd) / 2)):
                truncated.append(bsfDownEnd[n])
            index = truncated.index(max(truncated, key=itemgetter(1)))
            kEnd = truncated[index][0]

            # Get the starting position.
            truncated = []
            for n in range(int(len(bsfDownStart) / 2)):
                truncated.append(bsfDownStart[n])
            index = truncated.index(max(truncated, key=itemgetter(1)))
            kStart = truncated[index][0]

            # Calculate Fermi velocity.
            dk = kEnd - kStart
            vf = dE / dk
            I_vf.append(vf)
            concentrations.append(dirname)

            with open(outFile, 'a+') as f:
                f.write(dirname + ' ' + str(vf) + '\n')

            # Calculate time left.
            eachTimeTaken.append(time.time() - prevTime)
            prevTime = time.time()
            numDataLeft -= 1
            sys.stdout.write('\r' + str(numDataLeft) + '/' + str(numData)
                             + ' - Time left: ' + nmod.seconds2str(
                             nmod.findMean(eachTimeTaken) * numDataLeft)
                             + '         ')
            sys.stdout.flush()

        # Normalise the data and store as a new file.
        normalised = nmod.normalise(I_vf)
        print('\nNormalising Fermi velocity data...')
        with open(normalisedFile, 'a+') as f:
            for i in range(len(normalised)):
                f.write(concentrations[i] + ' ' + str(normalised[i]) + '\n')

        print('Fermi velocity analysis completed. Time taken: '
               + nmod.seconds2str(time.time() - startTime))

    def meanFreePath(self):
        """ Mean free path analysis """
        print('Running mean free path analysis...')
        concentrations = []
        I_mfp = []
        normalised = []
        outFile = os.path.join(self.analysisDir, 'mean_free_path.txt')
        normalisedFile = os.path.join(self.analysisDir,
                                      'mean_free_path_normalised.txt')

        checkAnalysisFiles(outFile, normalisedFile)

        # Define time variables for calculating time left.
        numData = len(self.listDataDir)
        numDataLeft = numData
        startTime = time.time()
        prevTime = startTime
        eachTimeTaken = []

        # Start the analysis process.
        for dirname in self.listDataDir:
            # Get the 2D BSF data at Fermi level.
            bsfDownFile = os.path.join(self.dataDir, dirname,
                                        '5_bsf2d_down.txt')
            rawFile = os.path.join(self.rawDir, dirname,
                                   dirname + '_5_BLOCHSF_spol.bsf')
            bsfDown = getBSF2D(bsfDownFile, rawFile, 'down', 5)

            # First crop half of the data to remove the other peak,
            # then get the position of the peak by finding the position of max.
            truncated = []
            for n in range(int(len(bsfDown) / 2)):
                truncated.append(bsfDown[n])
            index = truncated.index(max(truncated, key=itemgetter(1)))

            # Perform further cropping.
            dataDel = int(2*index - len(truncated))
            for n in range(dataDel):
                del truncated[0]

            nk = len(bsfDown)
            peakY = max(truncated, key=itemgetter(1))[1]
            peakX = truncated.index(peakY) / nk

            # Calculate mean free path.
            X = []
            for x, _ in truncated:
                X.append(x)
            popt, _ = curve_fit(lorentzian(peakX, peakY),
                                X, truncated, maxfev=1000)
            mfp = 1 / popt[0]
            I_mfp.append(mfp)
            concentrations.append(dirname)

            with open(outFile, 'a+') as f:
                f.write(dirname + ' ' + str(mfp) + '\n')

            # Calculate time left.
            eachTimeTaken.append(time.time() - prevTime)
            prevTime = time.time()
            numDataLeft -= 1
            sys.stdout.write('\r' + str(numDataLeft) + '/' + str(numData)
                             + ' - Time left: ' + nmod.seconds2str(
                             nmod.findMean(eachTimeTaken) * numDataLeft)
                             + '         ')
            sys.stdout.flush()

        # Normalise the data and store as a new file.
        normalised = nmod.normalise(I_mfp)
        print('\nNormalising mean free path data...')
        with open(normalisedFile, 'a+') as f:
            for i in range(len(normalised)):
                f.write(concentrations[i] + ' ' + str(normalised[i]) + '\n')

        print('Mean free path analysis completed. Time taken: '
               + nmod.seconds2str(time.time() - startTime))
