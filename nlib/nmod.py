""" Useful modules """
import os
import math

def chunks(l, size):
    """ Return same size chunks in a list """
    return [l[i:i+size] for i in range(0, len(l), size)]

def findLine(filename, s):
    """ Return first encountered line from a file with matching string """
    value = ""
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
    fmt = " " . join("{{:{}}}".format(x) for x in lens)
    return "\n" . join([fmt.format(*row) for row in s])

def float2str(prec, val):
    """ Return a nicely formatted string from a float """
    return "{val:.{prec}f}".format(prec=prec, val=val)

def storeFile(filename, text):
    """ Save text into a new file """
    try:
        os.remove(filename)
    except OSError:
        pass

    with open(filename, "a+") as f:
        f.write(text)

def nexit():
    """ Standard exit program function """
    print('Exiting program...')
    raise SystemExit
