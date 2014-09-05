#!/usr/bin/env python
""" Submit jobs """
import os
import sys
import inspect

# Add extra libraries' directories to import list
baseLibDir = os.path.join(os.path.realpath(os.path.dirname(
    inspect.getfile(inspect.currentframe()))), 'lib')

sys.path.append(baseLibDir)

# Import own libraries
from jobs import Jobs

if __name__ == '__main__':
    jobs = Jobs('CFMGS/B2')
    jobs.submitArray(1, 441, 10)
