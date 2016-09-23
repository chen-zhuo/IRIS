'''
This file contains functions of various algorithms.

@author: chen-zhuo
'''

import json
import shutil
import urllib.request

'''
Prints welcome message.
'''
def printWelcomeMsg():
    print()
    print('================================================================================')
    print()
    print('Welcome to IRIS.')
    print()
    print('IRIS (Indoor Route Instruction System) is a wearable device to provide')
    print('in-building navigation guidance for a visually-impaired person.')
    print()
    print('================================================================================')
    print()

'''
Downloads the map file from 'url' and save it locally as 'fileNameWithPath'.

@param url
           the URL of the file to be downloaded
@param fileNameWithPath
           e.g. '~/Desktop/IRIS/RaspberryPi/Downloads/mapOfCom1Storey2.json'
'''
def downloadMap(url, fileNameWithPath):
    with urllib.request.urlopen(url) as response, open(fileNameWithPath, 'wb') as file:
        shutil.copyfileobj(response, file)

'''
Waits for a keypad input from the user, and return the keypad input. A keypad input ends with a pound key ('#'). This
function blocks the function that calls this function.

@return a string representing the keypad input from the user (incl. the ending '#' character)
'''
def waitForKeypadInput():
    keypadInput = ''
#     while (not keypadInput.endswith('#')): # TODO
#         keypadInput += readKeypadInput()
    
    return keypadInput

def computeRoute():
    return

if __name__ == '__main__':
    pass
