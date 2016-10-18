'''
This is a unit-test file for path-finding.

@author: chen-zhuo
'''

from algorithms import computeRoute, downloadAndParseMap, linkMaps

def test():
    # COM1 Storey 2 student area --> COM2 Storey 3 mysterious pt
    srcBuildingId = 1
    srcBuildingStorey = 2
    srcNodeId = 11
    destBuildingId = 2
    destBuildingStorey = 3
    destNodeId = 16
    
    # to parse source and destination node IDs in the format of
    #     <buildingId><buildingStorey><originalNodeId (2 digits)>
    # . For example, COM1 Storey 2 Node #11 will be Node #1211.
    srcNodeId = srcBuildingId*1000 + srcBuildingStorey*100 + srcNodeId
    destNodeId = destBuildingId*1000 + destBuildingStorey*100 + destNodeId
    
    mapOfCom1Level1 = downloadAndParseMap('COM1', 1)
    mapOfCom1Level2 = downloadAndParseMap('COM1', 2)
    mapOfCom2Level2 = downloadAndParseMap('COM2', 2)
    mapOfCom2Level3 = downloadAndParseMap('COM2', 3)
    
    print('=============== Adjacency List for COM1 Storey 1 ===============\n')
    for node in mapOfCom1Level1.nodesDict.values():
        print(str(node.nodeId) + ': ' + str(sorted(list(node.adjacentNodes.keys()))))
        
    print('\n=============== Adjacency List for COM1 Storey 2 ===============\n')
    for node in mapOfCom1Level2.nodesDict.values():
        print(str(node.nodeId) + ': ' + str(sorted(list(node.adjacentNodes.keys()))))
    
    print('\n=============== Adjacency List for COM2 Storey 2 ===============\n')
    for node in mapOfCom2Level2.nodesDict.values():
        print(str(node.nodeId) + ': ' + str(sorted(list(node.adjacentNodes.keys()))))
    
    print('\n=============== Adjacency List for COM2 Storey 3 ===============\n')
    for node in mapOfCom2Level3.nodesDict.values():
        print(str(node.nodeId) + ': ' + str(sorted(list(node.adjacentNodes.keys()))))
    
    print('\n=============== Adjacency List for Linked Map ===============\n')
    linkedMap = linkMaps([mapOfCom1Level1, mapOfCom1Level2, mapOfCom2Level2, mapOfCom2Level3]);
    for node in linkedMap.nodesDict.values():
        print(str(node.nodeId) + ': ' + str(sorted(list(node.adjacentNodes.keys()))))
    print('\n==================================================\n')
    
    route = computeRoute(linkedMap, srcNodeId, destNodeId)
    print('Route: ', end='')
    for i in range(len(route) - 1):
        print(str(route[i]) + ' -> ', end = "")
    print(route[len(route) - 1])

if __name__ == '__main__':
    test()
