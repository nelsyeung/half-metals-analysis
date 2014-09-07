#!/usr/bin/env python3
""" Base jobs class for submitting multiple jobs """
import os
import inspect
import subprocess
import math
import time

# Import own libraries
import nmod

def checkRequired(mainDir, templatesDir, jobsDir):
    """ Check if the required directories and files exist """
    numJobs = 0 # For checking number of jobs in the jobs folder.
    error = False # Error flag for exiting program.

    if os.path.isdir(mainDir) is False:
        print('Templates directory does not exists, '
              'it is required to have the templates files at ')
        print(templatesDir + '.')
        error = True

    if os.path.isdir(templatesDir) is False:
        print('Templates directory does not exists, '
              'it is required to have the templates files at ')
        print(templatesDir + '.')
        error = True

    if os.path.isdir(jobsDir) is False:
        print('The directory provided does not have a jobs folder.')
        error = True
    else:
        # Check if there are any jobs in the new folder.
        newJobsDir = os.path.join(jobsDir, 'new')

        if os.path.isdir(newJobsDir) is True:
            os.chdir(newJobsDir)

            numJobs = len([name for name in os.listdir('./')
                          if os.path.isdir(name)])

    # Check if there are any jobs in the new folder.
    if numJobs == 0:
        print('No jobs in '
              + os.path.join(mainDir, 'jobs', 'new') + '.')
        print('Please make sure that your jobs are in that folder.')
        error = True

    return error

def submitSerial():
    """ Submit many serial jobs without overloading the task farm """

def submitArray(mainDir, pbsFile, start, end, **kwargs):
    """ Submit many array jobs without overloading the task farm """
    # Define all the required directories.
    baseDir = os.path.join(os.path.dirname(os.path.realpath(
        inspect.getfile(inspect.currentframe()))), '..')
    templatesDir = os.path.join(baseDir, 'templates')
    jobsDir = os.path.join(baseDir, mainDir, 'jobs')

    # Set default settings.
    settings = {
        'step': 10,
        'interval': 300
    }

    # Replace default settings with user defined settings.
    for key, value in kwargs.iteritems():
        settings[key] = value

    if checkRequired(mainDir, templatesDir, jobsDir):
        nmod.nexit()
    else:
        os.chdir(jobsDir)

    iterations = int(math.ceil((end - start) / settings['step']))
    last = iterations - 1 # Last iteration point for checks later.
    subCmd = ['qsub', pbsFile]
    checkInterval = settings['interval']

    timeStart = int(time.time())
    timePrev = timeStart

    # Submit the first batch of jobs.
    reps = {
        'tmpTSTART' : start,
        'tmpTEND'   : settings['step'] + start - 1
    }
    nmod.modFile(pbsFile,
        os.path.join(templatesDir, pbsFile), reps)
    subprocess.Popen(subCmd)

    for i in range(1, iterations):
        # Check if any jobs are still idle or blocked.
        # If there are, check again after an interval.
        # Only submit the next batch of jobs when there are no queued jobs.
        time.sleep(3) # Sleep to make sure the jobs are submitted.

        while True:
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
                timePrev = time.time()
                break
            else:
                print('There are still idle and blocked jobs after '
                      + nmod.seconds2str(time.time() - timePrev) + '.')
                timePrev = time.time()
                time.sleep(checkInterval) # Check jobs interval.


        # Submit the next batch of jobs.
        # Make sure the last iteration has the correct
        # ending point of -t (tempTEND).
        if i == last:
            print('Submitting -t ' + str(i * settings['step'] + start)
                  + '-' + str(end) + '...')
            reps = {
                'tmpTSTART' : i * settings['step'] + start,
                'tmpTEND'   : end
            }
        else:
            print('Submitting -t ' + str(i * settings['step'] + start)
                  + '-' + str((i+1) * settings['step'] + start - 1) + '...')
            reps = {
                'tmpTSTART' : i * settings['step'] + start,
                'tmpTEND'   : (i+1) * settings['step'] + start - 1
            }

        nmod.modFile(pbsFile,
            os.path.join(templatesDir, pbsFile), reps)
        subprocess.Popen(subCmd)

    timeTaken = nmod.seconds2str(time.time() - timeStart)
    print('All jobs submitted. Time taken: ' + timeTaken + '.')
