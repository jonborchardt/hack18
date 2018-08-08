import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
from legenderary.leGenderary import leGenderary

options = { 'male'          : 'male',
            'female'        : 'female',
            'androgynous'   : 'androgynous',
            'unknown'       : 'unknown',
            'maleConfirm'   : 'male needs confirmation',
            'femaleConfirm' : 'female needs confirmation',
            'dict1'         : 'legenderary/dict1.txt',
            'dict2'         : 'legenderary/dict2.txt',
            'customDict'    : 'legenderary/custom.txt',
            'bingAPIKey'    : 'ABC123478ZML'
          }

gender      = leGenderary(options)
fullName    = "Dr. Jane P. Feynman"

firstName   = gender.determineFirstName(fullName.split()) # Richard
dictionary  = gender.determineFromDictionary(firstName)   # male
takeaguess  = gender.randomGuess(firstName)               # male

#phonetic    = gender.determineFromPhonetic('Rikard')      # male
#soundex    = gender.determineFromSoundex('Rikard')
#nysiis     = gender.determineFromNysiis('Rikard')
#metaphone  = gender.determineFromMetaphone('Rikard')

#internet    = gender.determineFromInternet(fullName)      # male
#gPeters    = gender.determineFromGPeters(firstName)
#usebing    = gender.determineFromBing(fullName)

getgender   = gender.determineGender(fullName)            # male

print firstName, getgender                               # Richard, male
