""" Base compound class for generating different compounds """
import os
import sys
import inspect

# Add extra libraries' directories to import list
baseLibDir = os.path.join(os.path.realpath(os.path.dirname(
             inspect.getfile(inspect.currentframe()))), '..')
sys.path.append(baseLibDir)

# Import own libraries
import nmod

class Compound(object):
    """ Compound base class """
    def __init__(self, jobsDir, elements, potFile, alat):
        # Initialise all the required directories' path.
        baseDir = os.path.join(os.path.dirname(os.path.realpath(
            inspect.getfile(inspect.currentframe()))), '..', '..')
        self.templatesDir = os.path.join(baseDir, 'templates')
        self.jobsDir = os.path.join(baseDir, jobsDir, 'jobs', 'new')

        # Initialise the require information and settings.
        self.elements = elements.split()
        self.potFile = potFile
        self.potPath = os.path.join(self.templatesDir, potFile + '.pot')
        self.alat = alat
        self.settings = {
            'mode': 'SP-SREL',
            'nktab': '250',
            'ImE': '0.0005'
        }
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

        if (os.path.exists(self.potPath)
            is False):
            print('The potential file provided does not exists.')
            error = True

        if error:
            nmod.nexit()
        else:
            os.chdir(self.jobsDir)

    def modFile(self, new, tmp, reps):
        """ Copy and modify the specified template file to a new location """
        with open(new, "w+") as fnew:
            with open(os.path.join(self.templatesDir, tmp), "r") as ftmp:
                for line in ftmp:
                    fnew.write(nmod.replaceAll(line, reps))

    def create(self, conc):
        """ Create the specified compound """
        elementsFile = os.path.join(self.templatesDir, 'elements.txt')

        # Set the different concentrations
        concentrations = conc.split('_')
        conc1 = concentrations[0]
        conc2 = concentrations[1]
        conc3 = concentrations[2]
        conc4 = concentrations[3]
        conc5 = concentrations[4]

        # Set the different elements
        IT1 = nmod.findLine(elementsFile, self.elements[0])
        IT2 = nmod.findLine(elementsFile, self.elements[1])
        IT3 = nmod.findLine(elementsFile, self.elements[2])
        IT4 = nmod.findLine(elementsFile, self.elements[3])
        IT5 = nmod.findLine(elementsFile, self.elements[4])

        fullname = (
            self.elements[0] + conc1
            + self.elements[1] + conc2
            + self.elements[2] + conc3
            + self.elements[3] + conc4
            + self.elements[4] + conc5
        )
        mode = self.settings['mode']
        nktab = self.settings['nktab']
        ImE = self.settings['ImE']

        # Check if directory already exists, if not, carry on.
        if os.path.isdir(conc):
            print(conc + ' already exists, it will not be overwritten.')
        else:
            os.makedirs(conc)

            # Start the creation process.
            # Take all the template files, copy it to the new directory
            # and replace the "tmp" strings with the settings.

            # SCF
            reps = {
                "tmpDATASET" : fullname,
                "tmpMODE"    : mode,
                "tmpNKTAB"   : nktab
            }
            self.modFile(os.path.join(conc, 'scf.inp'), 'scf.inp', reps)

            # DOS
            reps = {
                "tmpDATASET" : fullname,
                "tmpMODE"    : mode,
                "tmpNKTAB"   : nktab,
                "tmpImE"     : ImE
            }
            self.modFile(os.path.join(conc, 'dos.inp'), 'dos.inp', reps)

            # POT
            reps = {
                "tmpSYSTEM" : fullname,
                "tmpALAT"   : self.alat,
                "tmpCONC1"  : conc1,
                "tmpCONC2"  : conc2,
                "tmpCONC3"  : conc3,
                "tmpCONC4"  : conc4,
                "tmpCONC5"  : conc5,
                "tmpIT1"    : IT1,
                "tmpIT2"    : IT2,
                "tmpIT3"    : IT3,
                "tmpIT4"    : IT4,
                "tmpIT5"    : IT5
            }
            self.modFile(os.path.join(conc, 'pot.pot'),
                         self.potFile + '.pot', reps)

            print(fullname + " has been created.")
