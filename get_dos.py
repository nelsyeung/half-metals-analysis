#!/usr/bin/env python
""" Get DOS data and move it to the data folder """
import os
import sys
import inspect

baseLibDir = os.path.join(os.path.realpath(os.path.dirname(
    inspect.getfile(inspect.currentframe()))), 'lib')

sys.path.append(baseLibDir)

# Import own libraries
import nmod

os.chdir(os.path.join('CFMGS', 'B2'))
cwd = os.getcwd()

for dirname in sorted(os.listdir('raw')):
    filePath = os.path.join(cwd, 'raw', dirname, 'dos.agr')
    nmod.getDOS(filePath, 'up')
    nmod.getDOS(filePath, 'down')

    if not os.path.isdir(os.path.join('data', dirname)):
        os.makedirs(os.path.join('data', dirname))

    os.rename(os.path.join('raw', dirname, 'dos_up.txt'),
              os.path.join('data', dirname, 'dos_up.txt'))

    os.rename(os.path.join('raw', dirname, 'dos_down.txt'),
              os.path.join('data', dirname, 'dos_down.txt'))
