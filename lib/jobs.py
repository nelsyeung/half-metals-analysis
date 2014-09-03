#!/usr/bin/env python3
""" Base jobs class for submitting multiple jobs """
import os
import sys
import inspect
import subprocess
import math
import time

# Import own libraries
import nmod

class Jobs(object):
    """ Jobs base class """
    def __init__(self, jobsDir):
        baseDir = os.path.join(os.path.dirname(os.path.realpath(
            inspect.getfile(inspect.currentframe()))), '..')
        self.templatesDir = os.path.join(baseDir, 'templates')
        self.jobsDir = os.path.join(baseDir, jobsDir, 'jobs')
        error = False # Error flag for exiting program.

        # Check if the required directories exist
        if os.path.isdir(self.templatesDir) is False:
            print('Templates directory does not exists, '
                  'it is required to have the templates files at ')
            print(self.templatesDir + '.')
            error = True

        if os.path.isdir(self.jobsDir) is False:
            print('The directory provided does not exists.')
            error = True
        else:
            # Check if there are any jobs in the new folder.
            os.chdir(os.path.join(self.jobsDir, 'new'))

            numJobs = len([name for name in os.listdir('./')
                          if os.path.isdir(name)])

            if numJobs == 0:
                print('No jobs in ' + os.path.join(jobsDir, 'jobs', 'new') + '.')
                print('Please make sure that your jobs are in that folder.')
                error = True

        if error:
            nmod.nexit()
        else:
            os.chdir(self.jobsDir)

    def modTemplateFile(self, new, tmp, reps):
        """ Copy and modify the specified template file to a new location """
        with open(new, 'w+') as fnew:
            with open(os.path.join(self.templatesDir, tmp), 'r') as ftmp:
                for line in ftmp:
                    fnew.write(nmod.replaceAll(line, reps))

    def submitArray(self, start, end, step):
        """ Submit many array jobs without overloading the task farm """
        iterations = int(math.ceil(end / step))
        last = iterations - 1 # Last iteration point for checks later.
        pbsFile = 'array_mpi.pbs'
        subCmd = ['qsub', pbsFile]
        queue = True # Initialise idle or blocked jobs are true.
        checkInterval = 900

        timeStart = int(time.time())
        timePrev = timeStart

        # Submit the first batch of jobs.
        reps = {
            'tmpTSTART' : start,
            'tmpTEND'   : step + start - 1
        }
        self.modTemplateFile(pbsFile, pbsFile, reps)
        subprocess.Popen(subCmd)

        time.sleep(10) # Sleep to make sure the jobs are submitted.

        for i in range(1, iterations):
            # Check if any jobs are still idle or blocked.
            # If there are, check again after an interval.
            # Only submit the next batch of jobs when there are no queued jobs.
            while queue:
                # Read in the showq command as an array separated by newline.
                p = subprocess.Popen(['showq', '-u', 'phukgm'],
                                     stdout = subprocess.PIPE,
                                     stderr = subprocess.PIPE)
                stdout, _ = p.communicate()
                stdout = stdout.decode()
                stdout = stdout.split('\n')

                # Check if queued jobs are non-zero.
                if ('Idle Jobs: 0' in stdout[-2]
                        and 'Blocked Jobs: 0' in stdout[-2]):
                    queue = False
                else:
                    queue = True
                    idleTime = nmod.seconds2str(int(time.time()) - timePrev)
                    timePrev = int(time.time())
                    print('There are still idle and blocked jobs after '
                          + idleTime + '.')
                    time.sleep(checkInterval) # Check jobs interval.

            # Submit the next batch of jobs.
            # Make sure the last iteration has the correct
            # ending point of -t (tempTEND).
            if i == last:
                print('Submitting -t ' + str(i * step + start)
                      + '-' + str(end) + '...')
                reps = {
                    'tmpTSTART' : i * step + start,
                    'tmpTEND'   : end
                }
            else:
                print('Submitting -t ' + str(i * step + start)
                      + '-' + str((i+1) * step + start - 1) + '...')
                reps = {
                    'tmpTSTART' : i * step + start,
                    'tmpTEND'   : (i+1) * step + start - 1
                }

            self.modTemplateFile(pbsFile, pbsFile, reps)
            subprocess.Popen(subCmd)

        timeTaken = nmod.seconds2str(int(time.time()) - timeStart)
        print('All jobs submitted. Time taken: ' + timeTaken + '.')
