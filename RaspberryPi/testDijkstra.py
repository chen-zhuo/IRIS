'''
This file is used for Week 7 demo of Dijkstra's algorithms.

@author: chen-zhuo
'''

from main import printWelcomeMsg
from mapAlgorithm import downloadMap

def testDijkstra():
    printWelcomeMsg()
    
    while True:
        print('\n=============== NEW TEST CASE ===============\n')
        buildingName = input('Enter building name: ')
        storey = input('Enter storey: ')
        startNodeId = input('Enter start node ID: ')
        endNodeId = input('Enter end node ID: ')
        
        try:
            url = 'http://showmyway.comp.nus.edu.sg/getMapInfo.php?Building=XXX&Level=YYY'
            url = url.replace('XXX', buildingName)
            url = url.replace('YYY', storey)
            print(url)
            fileName = 'mapOf' + buildingName.title() + "Storey" + storey + '.json'
            downloadMap(url, fileName)
        except:
            continue

if __name__ == '__main__':
    testDijkstra()
