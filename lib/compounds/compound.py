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
            'ImE': '0.0005',
            'SCF': {
                'NE': '30'
            },
            'DOS': {
                'NE': '50'
            },
            'BSF': {
                'NE': '1',
                'EMIN': '1.0',
                'EMAX': '1.0',
                'NK1': '60',
                'NK2': '60',
                'K1': '{1.0, 0.0, 0.0}',
                'K2': '{0.0, 1.0, 0.0}'
            }
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

    def modTemplateFile(self, new, tmp, reps):
        """ Copy and modify the specified template file to a new location """
        with open(new, 'w+') as fnew:
            with open(os.path.join(self.templatesDir, tmp), 'r') as ftmp:
                for line in ftmp:
                    fnew.write(nmod.replaceAll(line, reps))

    def create(self, fullConc):
        """ Create the specified compound """
        elementsFile = os.path.join(self.templatesDir, 'elements.txt')

        # Set the different concentrations
        concentrations = fullConc.split('_')
        conc = [None]*5
        for i in range(len(concentrations)):
            conc[i] = concentrations[i]

        # Set the different elements
        IT = [None]*5
        for i in range(len(self.elements)):
            IT[i] = nmod.findLine(elementsFile, self.elements[i])

        fullname = (
            self.elements[0] + conc[0]
            + self.elements[1] + conc[1]
            + self.elements[2] + conc[2]
            + self.elements[3] + conc[3]
            + self.elements[4] + conc[4]
        )

        # Check if directory already exists, if not, carry on.
        if os.path.isdir(fullConc):
            print(fullConc + ' already exists, it will not be overwritten.')
        else:
            os.makedirs(fullConc)

            # Start the creation process.
            # Take all the template files, copy it to the new directory
            # and replace the "tmp" strings with the settings.

            # POT
            reps = {
                'tmpSYSTEM' : fullname,
                'tmpALAT'   : self.alat,
                'tmpCONC1'  : conc[0],
                'tmpCONC2'  : conc[1],
                'tmpCONC3'  : conc[2],
                'tmpCONC4'  : conc[3],
                'tmpCONC5'  : conc[4],
                'tmpIT1'    : IT[0],
                'tmpIT2'    : IT[1],
                'tmpIT3'    : IT[2],
                'tmpIT4'    : IT[3],
                'tmpIT5'    : IT[4]
            }
            self.modTemplateFile(os.path.join(fullConc, 'pot.pot'),
                         self.potFile + '.pot', reps)

            # SCF
            reps = {
                'tmpDATASET' : fullname,
                'tmpMODE'    : self.settings['mode'],
                'tmpNKTAB'   : self.settings['nktab'],
                'tmpSCFNE'   : self.settings['SCF']['NE']
            }
            self.modTemplateFile(os.path.join(fullConc, 'scf.inp'), 'scf.inp', reps)

            print(fullname + " has been created.")

    def generateDOS(self):
        """ Generate DOS input files for all the compounds created """
        settingsDOS = self.settings['DOS']

        print('Generating DOS input files.')

        for _, dirs, _ in os.walk('./'):
            for directory in dirs:
                if (os.path.exists(os.path.join(directory, 'dos.inp'))
                        is True):
                    print(directory + ' already contains dos.inp, '
                          + 'it will not be overwritten.')
                else:
                    reps = {
                        'tmpDATASET' : directory,
                        'tmpMODE'    : self.settings['mode'],
                        'tmpNKTAB'   : self.settings['nktab'],
                        'tmpDOSNE'   : settingsDOS['NE'],
                        'tmpImE'     : self.settings['ImE']
                    }
                    self.modTemplateFile(os.path.join(directory, 'dos.inp'),
                                 'dos.inp', reps)

        print('Finish generating DOS input files.')

    def generateBSF(self):
        """ Generate BSF input files for all the compounds created """
        settingsBSF = self.settings['BSF']

        print('Generating BSF input files.')

        for _, dirs, _ in os.walk('./'):
            for directory in dirs:
                if (os.path.exists(os.path.join(directory, 'bsf.inp'))
                        is True):
                    print(directory + ' already contains bsf.inp, '
                          + 'it will not be overwritten.')
                else:
                    reps = {
                        'tmpDATASET' : directory,
                        'tmpNKTAB'   : self.settings['nktab'],
                        'tmpBSFNE'   : settingsBSF['NE'],
                        'tmpEMIN'    : settingsBSF['EMIN'],
                        'tmpEMAX'    : settingsBSF['EMAX'],
                        'tmpNK1'     : settingsBSF['NK1'],
                        'tmpNK2'     : settingsBSF['NK1'],
                        'tmpK1'      : settingsBSF['K1'],
                        'tmpK2'      : settingsBSF['K2']
                    }
                    self.modTemplateFile(os.path.join(directory, 'bsf.inp'),
                                 'bsf.inp', reps)

        print('Finish generating BSF input files.')
