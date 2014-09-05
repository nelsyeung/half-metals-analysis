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

        if (os.path.isfile(self.potPath) is False):
            print('The potential file provided does not exists.')
            error = True

        if error:
            nmod.nexit()
        else:
            os.chdir(self.jobsDir)

    def create(self, fullConc, **kwargs):
        """ Create the specified compound """
        elementsFile = os.path.join(self.templatesDir, 'elements.txt')

        # Set default settings.
        settings = {
            'mode'  : 'REL',
            'nktab' : '250',
            'NE'    : '30'
        }

        # Replace default settings with user defined settings.
        for key, value in kwargs.iteritems():
            settings[key] = value

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
            nmod.modFile(os.path.join(fullConc, 'pot.pot'),
                os.path.join(self.templatesDir, self.potFile + '.pot'), reps)

            # SCF
            reps = {
                'tmpDATASET' : fullname,
                'tmpMODE'    : settings['mode'],
                'tmpNKTAB'   : settings['nktab'],
                'tmpNE'      : settings['NE']
            }
            nmod.modFile(os.path.join(fullConc, 'scf.inp'),
                os.path.join(self.templatesDir, 'scf.inp'), reps)

            print(fullname + " has been created.")

    def generateDOS(self, **kwargs):
        """ Generate DOS input files for all the compounds created """
        # Set default settings.
        settings = {
            'mode'  : 'REL',
            'nktab' : '250',
            'NE'    : '50',
            'EMIN'  : '-0.2',
            'EMAX'  : '1.0',
            'ImE'   : '0.01'
        }

        # Replace default settings with user defined settings.
        for key, value in kwargs.iteritems():
            settings[key] = value

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
                        'tmpMODE'    : settings['mode'],
                        'tmpNKTAB'   : settings['nktab'],
                        'tmpNE'      : settings['NE'],
                        'tmpEMIN'    : settings['EMIN'],
                        'tmpEMAX'    : settings['EMAX'],
                        'tmpImE'     : settings['ImE']
                    }
                    nmod.modFile(os.path.join(directory, 'dos.inp'),
                        os.path.join(self.templatesDir, 'dos.inp'), reps)

        print('Finish generating DOS input files.')

    def generateBSF(self, **kwargs):
        """ Generate BSF input files for all the compounds created """
        settings = {
            'nktab' : '250',
            'NE'    : '1',
            'EMIN'  : '1.0',
            'EMAX'  : '1.0',
            'NK1'   : '60',
            'NK2'   : '60',
            'K1'    : '{1.0, 0.0, 0.0}',
            'K2'    : '{0.0, 1.0, 0.0}'
        }

        # Replace default settings with user defined settings.
        for key, value in kwargs.iteritems():
            settings[key] = value

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
                        'tmpNKTAB'   : settings['nktab'],
                        'tmpNE'      : settings['NE'],
                        'tmpEMIN'    : settings['EMIN'],
                        'tmpEMAX'    : settings['EMAX'],
                        'tmpNK1'     : settings['NK1'],
                        'tmpNK2'     : settings['NK1'],
                        'tmpK1'      : settings['K1'],
                        'tmpK2'      : settings['K2']
                    }
                    nmod.modFile(os.path.join(directory, 'bsf.inp'),
                         os.path.join(self.templatesDir, 'bsf.inp'), reps)

        print('Finish generating BSF input files.')
