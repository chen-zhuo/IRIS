'''
This file contains functions of various algorithms.

@author: chen-zhuo
'''

import json
import shutil
import urllib.request

import Map

'''
Prints welcome message.
'''
def printWelcomeMsg():
    print('\n================================================================================\n')
    print('Welcome to IRIS.\n')
    print('IRIS (Indoor Route Instruction System) is a wearable device to provide')
    print('in-building navigation guidance for a visually-impaired person.\n')
    print('================================================================================\n')

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
Waits for a keypad input from the user, and returns the keypad input. A keypad input ends with a pound key ('#'). This
function blocks the function that calls this function.

@return a string representing the keypad input from the user (incl. the ending '#' character)
'''
def waitForKeypadInput():
    keypadInput = ''
#     while (not keypadInput.endswith('#')): # TODO
#         keypadInput += readKeypadInput()
    
    return keypadInput

'''
@param rawMapInfo:
           a json object representing the map
@return a 'Map' object
'''
def parseMapInfo(rawMapInfo):
    processedMapInfo = Map()
    # TODO
    return processedMapInfo

def computeRoute():
    return

def dijkstra():
    return

def relax():
    return

if __name__ == '__main__':
    pass
