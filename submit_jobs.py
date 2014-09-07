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
import jobs

if __name__ == '__main__':
    jobs.submitArray('CFMGS/B2', 'array_mpi_bsf.pbs', 1, 441,
                     step=10, interval=60)
