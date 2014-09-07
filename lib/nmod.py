""" Useful and shared functions """
import os
import math
import numpy as np
from scipy.interpolate import interp1d

def chunks(l, size):
    """ Return same size chunks in a list """
    return [l[i:i+size] for i in range(0, len(l), size)]

def findLine(filename, s):
    """ Return first encountered line from a file with matching string """
    value = ''
    with open(filename, "r") as f:
        for line in f:
            if s in line:
                value = line
                break
    return value

def findMean(l):
    """ Find the mean of a list """
    return math.fsum(l) / len(l)

def replaceAll(text, reps):
    """ Replace all the matching strings from a piece of text """
    for i, j in reps.items():
        text = text.replace(str(i), str(j))
    return text

def ntabulate(matrix):
    """ Return a nice tabulated string from a matrix """
    s = [[str(e) for e in row] for row in matrix]
    lens = [len(max(col, key=len)) for col in zip(*s)]
    fmt = ' ' . join('{{:{}}}'.format(x) for x in lens)
    return '\n' . join([fmt.format(*row) for row in s])

def float2str(prec, val):
    """ Return a nicely formatted string from a float """
    return '{val:.{prec}f}'.format(prec=prec, val=val)

def nexit():
    """ Standard exit program function """
    print('Exiting program...')
    raise SystemExit

def seconds2str(s):
    """ Return a nicely formatted time string from seconds """
    seconds = str(int(s % 60))
    minutes = str(int(s / 60) % 60)
    hours = str(int(s / 3600))
    return hours + 'h ' + minutes + 'm ' + seconds + 's'

def modFile(new, tmp, reps):
    """ Copy and modify the specified file to a new location """
    with open(new, 'w+') as fnew:
        with open(tmp, 'r') as ftmp:
            for line in ftmp:
                fnew.write(replaceAll(line, reps))

def getDOS(filePath, spin):
    """ Store into text file and return DOS data """
    baseDir = os.path.dirname(os.path.abspath(filePath))
    filename = os.path.basename(filePath).split('.')[0]
    outFile = os.path.join(baseDir, filename + '_' + spin + '.txt')
    dos = []
    record = False

    if spin == 'up':
        dataStart = '@target G0.S0'
    elif spin == 'down':
        dataStart = '@target G1.S0'
    else:
        print('Incorrect spin.')
        nexit()

    with open(filePath) as f:
        for l in f:
            line = l.rstrip()

            if line == dataStart:
                record = True
                continue

            if line == '&':
                record = False
                continue

            if record and not '@' in line:
                x = float(line.split()[0])
                y = float(line.split()[1])
                dos.append([x, y])

    if os.path.isfile(outFile) is True:
        os.remove(outFile)

    with open(outFile, 'a+') as f:
        for x, y in dos:
            f.write(str(x) + ' ' + str(y) + '\n')

    return dos

def getBSF3D(filePath, spin, numSites):
    """ Store into text file and return 3D BSF data """
    baseDir = os.path.dirname(os.path.abspath(filePath))
    bsfnum = os.path.basename(filePath).split('_')[-2]
    if bsfnum.isdigit() == True:
        outFile = os.path.join(baseDir, bsfnum + '_bsf3d_' + spin + '.txt')
    else:
        outFile = os.path.join(baseDir, 'bsf3d_' + spin + '.txt')
    raw = []
    hashCount = 0 # For determining when to start reading raw data.

    # Get raw data first.
    with open(filePath) as f:
        for l in f:
            line = l.rstrip()

            if '###' in line:
                hashCount += 1
                continue

            if hashCount == 3:
                x = float(line.split()[0])
                y = float(line.split()[1])
                raw.append([x, y])

    # Generate plotable data from raw
    numUseful = (numSites - 1) * 2
    nk = len(raw) / numUseful
    nk2 = nk * nk
    bsf = [[] for i in range(nk)]

    if spin == 'up':
        sign = -1
    elif spin == 'down':
        sign = 1

    for i in range(nk2):
        n = math.floor(i / nk)
        j = i + (nk2 * numUseful - 2)
        bsf[n].append(float(raw[i]) + sign * float(raw[j]))

    if os.path.isfile(outFile) is True:
        os.remove(outFile)

    np.savetxt(outFile, bsf)

    return bsf

def getBSF2D(filePath, spin, numSites):
    """ Store into text file and return single strip of BSF data """
    baseDir = os.path.dirname(os.path.abspath(filePath))
    bsfnum = os.path.basename(filePath).split('_')[-2]
    if bsfnum.isdigit() == True:
        outFile = os.path.join(baseDir, bsfnum + '_bsf2d_' + spin + '.txt')
    else:
        outFile = os.path.join(baseDir, 'bsf2d_' + spin + '.txt')
    bsf3D = getBSF3D(filePath, spin, numSites)
    bsf = []
    nk = len(bsf3D)

    for i in range(nk):
        bsf.append([ i / nk, bsf3D[0][i]])

    if os.path.isfile(outFile) is True:
        os.remove(outFile)

    with open(outFile, 'a+') as f:
        for x, y in bsf:
            f.write(str(x) + ' ' + str(y) + '\n')

    return bsf

def getInterp1d(data):
    """ Get interpolated data from a list with x and y values """
    x, y = [], []

    for X, Y in data:
        x.append(X)
        y.append(Y)

    return interp1d(x, y)

def normalise(inp):
    """ Linearly normalise the input values to range from 0 to 1 """
    normalised = []
    xmin = min(inp)
    xmax = max(inp)

    for x in inp:
        normalised.append((x - xmin) / (xmax - xmin))

    return normalised
