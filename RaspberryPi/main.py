'''
This file contains the 'main()' function, which is the starting point of the program. High-level algorithms such as task
scheduling, thread instantiations, are defined here.

@author: chen-zhuo
'''

import json
import threading

from algorithms import downloadMap
from algorithms import printWelcomeMsg
from pprint import pprint

def main():
    printWelcomeMsg()
    
    url = 'http://showmyway.comp.nus.edu.sg/getMapInfo.php?Building=COM1&Level=2'
    fileName = './Downloads/mapOfCom1Storey2.json'
    
    downloadMap(url, fileName)
    
    # to open a file named 'fileName' as json file
    with open(fileName) as jsonFile:
        mapInfoRaw = json.load(jsonFile)
    
    northAt = mapInfoRaw['info']['northAt']
    nodesList = mapInfoRaw['map']
    
    node1X = mapInfoRaw['map'][0]['nodeId']
    
    pprint(mapInfoRaw)
    print('northAt: ' + northAt)
#     print('Map: ' + nodesList[0])
    
    print(node1X)

if __name__ == '__main__':
    main()
