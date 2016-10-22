'''
This file defines the `Navigator` object class.

@author: chen-zhuo
'''

import algorithms
import Map
import math
import stringHelper
import audioOutput

class Navigator():
    def __init__(self, myMap, route, currentX, currentY):
        self.myMap = myMap
        self.route = route # a list of node IDs
        self.clearedRouteIdx = 0 # if 'clearedRouteIdx == 3', then the user has cleared the node ID 'route[3]'
        self.currentX = currentX
        self.currentY = currentY
        self.currentBearing = 0
        self.threshold = 200
    
    def updateLocation(self, currentX, currentY, currentBearing):
        self.currentX = currentX
        self.currentY = currentY
        self.currentBearing = currentBearing
        
        if algorithms.computeDistance(self.currentX, self.currentY,
                self.myMap.getNode(self.route[self.clearedRouteIdx + 1]).x,
                self.myMap.getNode(self.route[self.clearedRouteIdx + 1]).y) < self.threshold:
            self.currentX = self.myMap.getNode(self.route[self.clearedRouteIdx + 1]).x
            self.currentY = self.myMap.getNode(self.route[self.clearedRouteIdx + 1]).y
            self.clearedRouteIdx = self.clearedRouteIdx + 1
            print(stringHelper.AUDIO + ' Reached node Id: #' + str(self.route[self.clearedRouteIdx]))
            audioOutput.playAudio('reachedNewNodeSoundEffect')
            audioOutput.playAudio('reached')
            audioOutput.playAudio('nodeId')
            audioOutput.playInt(self.route[self.clearedRouteIdx])
    
    def getNaviInfo(self):
        distance = algorithms.computeDistance(self.currentX, self.currentY,
                self.myMap.getNode(self.route[self.clearedRouteIdx + 1]).x,
                self.myMap.getNode(self.route[self.clearedRouteIdx + 1]).y)
        bearing = algorithms.computeBearing(self.currentX, self.currentY,
                self.myMap.getNode(self.route[self.clearedRouteIdx + 1]).x,
                self.myMap.getNode(self.route[self.clearedRouteIdx + 1]).y)
        return (distance, bearing)

if __name__ == '__main__':
    pass
