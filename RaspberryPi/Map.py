'''
This file defines the `Map` and `Node` object classes. A `Map` object consists of a set of interconnected `Node` objects
with known locations. A `Map` contains information for one storey of a particular building.

@author: chen-zhuo
'''

import stringHelper

class Map:
    def __init__(self, buildingId, buildingName, buildingStorey, northAt):
        self.buildingId = buildingId # e.g. 1
        self.buildingName = buildingName # e.g. 'COM1'
        self.buildingStorey = buildingStorey # e.g. 2
        self.northAt = northAt # e.g. 315; the bearing of geographical north to 0 degree of this map
        
        self.nodesDict = {} # to map `nodeId` (key) to its corresponding `node` object (value)
    
    def __iter__(self):
        return iter(self.nodesDict.values())
    
    def addNode(self, node):
        self.nodesDict[node.nodeId] = node
    
    def getNode(self, nodeId):
        if nodeId in self.nodesDict:
            return self.nodesDict[nodeId]
        else:
            raise ValueError('Node #' + nodeId + ' does not exist.')
            return None
    
    def addEdge(self, srcNodeId, destNodeId, weight=0):
        if srcNodeId not in self.nodesDict:
            print(stringHelper.ERROR + ' at Map.addEdge(): \'srcNodeId\' #' + str(srcNodeId) + 'does not exist.')
        elif destNodeId not in self.nodesDict:
            print(stringHelper.ERROR + ' at Map.addEdge(): \'destNodeId\' #' + str(destNodeId) + 'does not exist.')
        else:
            self.nodesDict[srcNodeId].addNeighbor(destNodeId, weight)
            self.nodesDict[destNodeId].addNeighbor(srcNodeId, weight)
    
    def getNodeIds(self):
        return self.nodesDict.keys()

class Node:
    def __init__(self, nodeId, nodeName, x, y):
        self.nodeId = nodeId
        self.nodeName = nodeName
        self.x = x # x-coordinate (in cm) of this node
        self.y = y # y-coordinate (in cm) of this node
        
        self.adjacentNodes = {} # if `adjacentNodes[6]` is 1000, that means this node is connected to node 6 (`nodeId`
                                # is 6), and they are 1000 cm apart (a.k.a. 'edge weight')
    
    def addNeighbor(self, neighborNodeId, weight=0):
        self.adjacentNodes[neighborNodeId] = weight
    
    def getNeighbors(self):
        return self.adjacentNodes.keys()
    
    def getWeight(self, neighborNodeId):
        return self.adjacentNodes[neighborNodeId]
    
    def __str__(self):
        return 'Node #' + str(self.nodeId) + ': \'' + self.nodeName + '\'; ' + \
                'adjacent nodes: ' + str(self.adjacentNodes)

if __name__ == '__main__':
    pass
