'''
This file defines the `Navigator` object class.

@author: chen-zhuo
'''

import algorithms
import Map
import math
import stringHelper
import audioOutput

STEP_LENGTH = 40

class Navigator():
    def __init__(self, myMap, route, currLocation):
        self.myMap = myMap
        self.route = route # a list of node IDs
        self.srcNodeId = route[0]
        self.destNodeId = route[len(route) - 1]
        self.clearedRouteIdx = 0 # if `clearedRouteIdx == 3`, then the user has cleared the node ID `route[3]`
        self.distanceUntilNextNode = algorithms.computeDistance(myMap.nodesDict[route[0]].location,
                                                                myMap.nodesDict[route[1]].location)
        self.nodeReachedThreshold = 100
        
        self.currLocation = currLocation
        self.locationOffset = [0, 0]
        
        self.currHeading = 0
        self.expectedHeading = 0
    
    '''
    Updates the fields of `self`.
    
    @param dataPacket
           the data packet received from Mega
    @return False if the last node in `route` is cleared; else return True
    '''
    def update(self, dataPacket):
        global STEP_LENGTH
        
        # if the last node is cleared then return False
        if self.clearedRouteIdx == len(self.route) - 1:
            print(stringHelper.AUDIO + ' Navigation completed.')
            audioOutput.playAudio('navigationCompleted')
            return False
        
        # to calculate the current location based on the distances travelled in 8 directions, as well as the offset
        self.currLocation = self.myMap.nodesDict[self.srcNodeId].location
        self.currLocation[0] -= dataPacket.distancesList[0]/math.sqrt(2)
        self.currLocation[1] += dataPacket.distancesList[0]/math.sqrt(2)
        self.currLocation[1] += dataPacket.distancesList[1]
        self.currLocation[0] += dataPacket.distancesList[2]/math.sqrt(2)
        self.currLocation[1] += dataPacket.distancesList[2]/math.sqrt(2)
        self.currLocation[0] += dataPacket.distancesList[3]
        self.currLocation[0] += dataPacket.distancesList[4]/math.sqrt(2)
        self.currLocation[1] -= dataPacket.distancesList[4]/math.sqrt(2)
        self.currLocation[1] -= dataPacket.distancesList[5]
        self.currLocation[0] -= dataPacket.distancesList[6]/math.sqrt(2)
        self.currLocation[1] -= dataPacket.distancesList[6]/math.sqrt(2)
        self.currLocation[0] -= dataPacket.distancesList[7]
        self.currLocation[0] += self.locationOffset[0]
        self.currLocation[1] += self.locationOffset[1]
        
        # to print the current location (absolute coordinates and relative coordinates from starting location)
        print(stringHelper.INFO + ' currLocation = (' +
              str(self.currLocation[0]) + ',' + str(self.currLocation[1]) + '), ' +
              'displacementFromStartingLocation = (' +
              str(self.currLocation[0] - self.myMap.nodesDict[self.srcNodeId].location[0]) + ',' +
              str(self.currLocation[1] - self.myMap.nodesDict[self.srcNodeId].location[1]) + ')')
        
        self.distanceUntilNextNode = algorithms.computeDistance(self.currLocation,
                self.myMap.getNode(self.route[self.clearedRouteIdx + 1]).location)
        
        self.expectedHeading = algorithms.computeBearing(self.currLocation,
                self.myMap.getNode(self.route[self.clearedRouteIdx + 1]).location)
        
        self.currHeading = dataPacket.heading
        
        # if current location is within nodeReachedThreshold of the next node in `route`, then update `clearedRouteIdx`
        if algorithms.computeDistance(self.currLocation,
                self.myMap.getNode(self.route[self.clearedRouteIdx + 1]).location) < self.nodeReachedThreshold:
#             self.currX = self.myMap.getNode(self.route[self.clearedRouteIdx + 1]).x
#             self.currY = self.myMap.getNode(self.route[self.clearedRouteIdx + 1]).y
            self.clearedRouteIdx = self.clearedRouteIdx + 1
            print(stringHelper.AUDIO + ' Reached node Id: #' + str(self.route[self.clearedRouteIdx]))
            audioOutput.playAudio('reachedNewNodeSoundEffect')
            audioOutput.playAudio('reached')
            audioOutput.playInt(self.route[self.clearedRouteIdx])
        
        return True # `isNavigationInProgress` is True
    
    '''
    to give turning instructions; with C major scale (1 = C4),
        - "3" means "go straight";
        - "1" means "turn left 45 degrees";
        - "5" means "turn right 45 degrees";
        - "11" means "turn left 90 degrees";
        - "55" means "turn right 90 degrees";
        - "111" means "turn left 135 degrees";
        - "555" means "turn right 135 degrees";
        - "1(+8va)" means "turn 180 degrees"
    '''
    def playHeadingAdjustmentAudioFeedback(self):
        if self.expectedHeading - self.currHeading == 0:
            print(stringHelper.AUDIO + ' Adjust heading: 0 degree')
            audioOutput.playAudioNow('heading+0_soundEffect')
        elif self.expectedHeading - self.currHeading == -45 or self.expectedHeading - self.currHeading == 315:
            print(stringHelper.AUDIO + ' Adjust heading: -45 degrees')
            audioOutput.playAudioNow('heading-45_soundEffect')
        elif self.expectedHeading - self.currHeading == 45 or self.expectedHeading - self.currHeading == -315:
            print(stringHelper.AUDIO + ' Adjust heading: +45 degrees')
            audioOutput.playAudioNow('heading+45_soundEffect')
        elif self.expectedHeading - self.currHeading == -90 or self.expectedHeading - self.currHeading == 270:
            print(stringHelper.AUDIO + ' Adjust heading: -90 degrees')
            audioOutput.playAudioNow('heading-90_soundEffect')
        elif self.expectedHeading - self.currHeading == 90 or self.expectedHeading - self.currHeading == -270:
            print(stringHelper.AUDIO + ' Adjust heading: +90 degrees')
            audioOutput.playAudioNow('heading+90_soundEffect')
        elif self.expectedHeading - self.currHeading == -135 or self.expectedHeading - self.currHeading == 225:
            print(stringHelper.AUDIO + ' Adjust heading: -135 degrees')
            audioOutput.playAudioNow('heading-135_soundEffect')
        elif self.expectedHeading - self.currHeading == 135 or self.expectedHeading - self.currHeading == -225:
            print(stringHelper.AUDIO + ' Adjust heading: +135 degrees')
            audioOutput.playAudioNow('heading+135_soundEffect')
        elif self.expectedHeading - self.currHeading == 180 or self.expectedHeading - self.currHeading == -180:
            print(stringHelper.AUDIO + ' Adjust heading: 180 degrees')
            audioOutput.playAudioNow('heading+180_soundEffect')
        else:
            print(stringHelper.ERROR + ' at main(): Unhandled case of heading adjustment; expectedHeading - \
                  dataPacket.heading = ' + str(self.expectedHeading - self.currHeading))

if __name__ == '__main__':
    pass
