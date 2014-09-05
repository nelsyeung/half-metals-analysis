""" Useful and shared functions """
import os
import math
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
    return math.fsum(l) / float(len(l))

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
    seconds = str(s % 60)
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
    DOS = []
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
                DOS.append([x, y])

    if os.path.isfile(outFile) is True:
        os.remove(outFile)

    with open(outFile, 'a+') as f:
        for x, y in DOS:
            f.write(str(x) + ' ' + str(y) + '\n')

    return DOS

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
