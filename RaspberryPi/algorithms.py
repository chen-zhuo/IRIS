'''
This file contains functions of various algorithms.

@author: chen-zhuo
'''

import copy
import heapq
import json
from Map import Map, Node
import math
import shutil
from time import sleep
import urllib.request
import stringHelper

buildingDict = {'COM1': 1, 'COM2': 2} # to map `buildingName` to the corresponding `buildingId`

# for modified Dijkstra's algorithm
pq = [] # priority queue; stores tuples `(displacement, nodeId)`
displacement = {} # if `displacement[i] == 1000`, then the displacement of node `i` from the source node is 1000 cm
hasVisited = {} # if `hasVisited[i] == True`, then node `i` has been visited
parentOf = {} # if `parentOf[i] == j`, then node `j` is node `i`'s parent
route = []

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
Downloads a map file from the Internet and save it locally in the path './Downloads/'. Next, parse the file into a `Map`
object and return it. If there is no internet connection, use the cached map file from './Downloads/Caches/'.

@param buildingName
           the building name of the map file to be downloaded, e.g. 'COM1'
@param buildingStorey
           the storey of the map file to be downloaded, e.g. 2
@return the parsed `Map` object
'''
def downloadAndParseMap(buildingName, buildingStorey):
    url = 'http://showmyway.comp.nus.edu.sg/getMapInfo.php?Building=XXX&Level=YYY'
    url = url.replace('XXX', str(buildingName))
    url = url.replace('YYY', str(buildingStorey))
    print(url)
    fileName = 'mapOf' + str(buildingName) + 'Storey' + str(buildingStorey) + '.json'
    
    # to download map from Internet; if no Internet access, use cached map
#     try:
#         fileNameWithPath = './Downloads/' + fileName
#         with urllib.request.urlopen(url) as response, open(fileNameWithPath, 'wb') as file:
#             shutil.copyfileobj(response, file)
#         with open(fileNameWithPath) as jsonFile:
#             rawMap = json.load(jsonFile)
#     except IOError:
#         fileNameWithPath = './Downloads/Caches/' + fileName
#         with open(fileNameWithPath) as jsonFile:
#             rawMap = json.load(jsonFile)
    fileNameWithPath = './Downloads/Caches/' + fileName
    with open(fileNameWithPath) as jsonFile:
        rawMap = json.load(jsonFile)
    
    buildingId = buildingDict[buildingName]
    northAt = int(rawMap['info']['northAt'])
    myMap = Map(buildingId, buildingName, buildingStorey, northAt)
    
    # to populate `Node` objects in `myMap`, except edge information (i.e. do not connect the nodes yet)
    for i in range(len(rawMap['map'])):
        nodeId = int(rawMap['map'][i]['nodeId'])
        nodeName = rawMap['map'][i]['nodeName']
        x = int(rawMap['map'][i]['x'])
        y = int(rawMap['map'][i]['y'])
        myNode = Node(nodeId, nodeName, x, y)
        myMap.addNode(myNode)
    
    # to update edge information (i.e. to connect the nodes) in `myMap`
    for i in range(len(rawMap['map'])):
        nodeId = int(rawMap['map'][i]['nodeId'])
        neighborNodeIds = rawMap['map'][i]['linkTo'].replace(' ', '').split(',') # warning: type is str[]
        for neighborNodeId in neighborNodeIds:
            neighborNodeId = int(neighborNodeId)                                 # cast to int
            weight = computeDistance(myMap.getNode(nodeId).x, myMap.getNode(nodeId).y,
                                     myMap.getNode(neighborNodeId).x, myMap.getNode(neighborNodeId).y)
            myMap.getNode(nodeId).adjacentNodes[neighborNodeId] = weight
    
    return myMap

def linkMaps(mapsList):
    resultMap = Map(None, None, None, 0)
    
    for aMap in mapsList:
        for node in aMap.nodesDict.values():
            modifiedNode = copy.deepcopy(node)
            modifiedNode.nodeId += aMap.buildingId*1000 + aMap.buildingStorey*100
            modifiedNode.adjacentNodes.clear()
            
            for oldAdjacentNodeId in node.adjacentNodes.keys():
                newAdjacentNodeId = aMap.buildingId*1000 + aMap.buildingStorey*100 + oldAdjacentNodeId
                modifiedNode.adjacentNodes[newAdjacentNodeId] = node.adjacentNodes[oldAdjacentNodeId]
            
            resultMap.addNode(modifiedNode)
    
    # to link COM1 storey 2 to COM2 storey 2
    resultMap.addEdge(1231, 2201, 0)
    resultMap.addEdge(2201, 1231, 0)
      
    # to link COM2 storey 2 to COM2 storey 3
    resultMap.addEdge(2216, 2311, 0)
    resultMap.addEdge(2311, 2216, 0)
    
    resultMap.getNode(1101).adjacentNodes[1101] = 0
    
    return resultMap

def computeRoute(myMap, srcNodeId, destNodeId):
    global route
    
    dijkstra(myMap, srcNodeId)
    route = []
    populateRoute(destNodeId)
    return route

def computeDistance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def dijkstra(myMap, srcNodeId):
    global pq, displacement, hasVisited, parentOf
    pq = []
    displacement = {}
    hasVisited = {}
    parentOf = {}
    
    for node in myMap:
        displacement[node.nodeId] = float('inf')
        hasVisited[node.nodeId] = False
        parentOf[node.nodeId] = None
    
    displacement[srcNodeId] = 0
    pq.append((displacement[srcNodeId], srcNodeId))
    heapq.heapify(pq)
    
    while len(pq) > 0:
        nextInQueue = heapq.heappop(pq)
        
        # skip `nextInQueue` if it is invalid
        if nextInQueue[0] > displacement[nextInQueue[1]]:
            continue
        
        for neighborNodeId in myMap.getNode(nextInQueue[1]).adjacentNodes.keys():
            relax(nextInQueue[1], neighborNodeId, myMap.getNode(nextInQueue[1]).adjacentNodes[neighborNodeId])
    
    return parentOf

def relax(nodeId, neighborNodeId, weight):
    global pq, displacement, hasVisited, parentOf
    
    if displacement[neighborNodeId] > displacement[nodeId] + weight:
        displacement[neighborNodeId] = displacement[nodeId] + weight
        parentOf[neighborNodeId] = nodeId
        pq.append((displacement[neighborNodeId], neighborNodeId))
        heapq.heapify(pq)

'''
Recursively updates the global variable `route` using the global variable `parentOf`.
Precondition: The global variable `route` must be cleared before calling this function.

@param destNodeId
           destination node ID
'''
def populateRoute(destNodeId):
    global parentOf, route
    
    if parentOf[destNodeId] != None:
        populateRoute(parentOf[destNodeId])
    route.append(destNodeId)

'''
Computes the bearing of point B from point A.

@param x1
           x-coordinate of point A
@param y1
           y-coordinate of point A
@param x2
           x-coordinate of point B
@param y2
           y-coordinate of point B
@return the bearing of point B from point A
'''
def computeBearing(x1, y1, x2, y2):
    if x2 == x1 and y2 == y1:
        return 0
    elif x2 == x1 and y2 > y1:
        return 0
    elif x2 == x1 and y2 < y1:
        return 180
    elif y2 == y1 and x2 > x1:
        return 90
    elif y2 == y1 and x2 < x1:
        return 270
    elif x2 > x1 and y2 > y1: # first quadrant
        return math.degrees(math.atan((x2 - x1)/(y2 - y1)))
    elif x2 < x1 and y2 > y1: # second quadrant
        return 360 - math.degrees(math.atan((x1 - x2)/(y2 - y1)))
    elif x2 < x1 and y2 < y1: # third quadrant
        return 180 + math.degrees(math.atan((x1 - x2)/(y1 - y2)))
    else: # fourth quadrant
        return 180 - math.degrees(math.atan((x2 - x1)/(y1 - y2)))










'''
@todo

Waits for a keypad input from the user, and returns the keypad input. A keypad input ends with a hash key ('#'). This
function blocks the function that calls this function.

@return a string representing the keypad input from the user (incl. the ending '#' character)
'''
def waitForKeypadInput():
    keypadInput = ''
    while (not keypadInput.endswith('#')):
        keypadInput += _readKeypadInput()
    
    return keypadInput

def _readKeypadInput():
    return




if __name__ == '__main__':
    pass
