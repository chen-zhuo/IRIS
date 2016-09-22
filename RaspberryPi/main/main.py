'''
This file contains the 'main()' function, which is the starting point of the program. High-level algorithms such as task
scheduling, thread instantiations, are defined here.
'''

import json
import shutil
import threading
import urllib.request

from pprint import pprint

def main():
    printWelcomeMsg()
    
    url = 'http://showmyway.comp.nus.edu.sg/getMapInfo.php?Building=COM1&Level=2'
    fileName = 'mapOfCom1Storey2.json'
    
    downloadFile(url, fileName)
    
    # to open a file named 'fileName' as json file
    with open(fileName) as jsonFile:
        mapInfoRaw = json.load(jsonFile)
    
    northAt = mapInfoRaw['info']['northAt']
    nodesList = mapInfoRaw['map']
    
    node1X = mapInfoRaw['map'][0]['nodeId']
    
    pprint(mapInfoRaw)
    print('northAt: ' + northAt)
#     print('map: ' + nodesList[0])
    
    print(node1X)

# Downloads the file from 'url' and save it locally as 'fileName'.
def downloadFile(url, fileName):
    with urllib.request.urlopen(url) as response, open(fileName, 'wb') as file:
        shutil.copyfileobj(response, file)

# Prints welcome message.
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

if __name__ == '__main__':
    main()
