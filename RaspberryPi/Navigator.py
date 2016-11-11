'''
This file defines the `Navigator` object class.

@author: chen-zhuo
'''

import algorithms
import copy
import Map
import math
import stringHelper
import audioOutput

IS_SNAP_TO_GRAPH_EDGE = False
STEP_LENGTH = 58
NODE_REACHED_THRESHOLD = 100

class Navigator():
    def __init__(self, myMap, route):
        self.myMap = myMap
        self.route = route # a list of node IDs
        self.srcNodeId = route[0]
        self.destNodeId = route[len(route) - 1]
        self.clearedRouteIdx = 0 # if `clearedRouteIdx == 3`, then the user has cleared the node ID `route[3]`
        self.distanceUntilNextNode = algorithms.computeDistance(myMap.nodesDict[route[0]].location,
                                                                myMap.nodesDict[route[1]].location)
        
        self.currLocation = copy.deepcopy(self.myMap.nodesDict[self.srcNodeId].location)
        
        self.initialHeading = 0
        self.currHeading = 0
#         self.prevHeading = 0
        self.expectedHeading = 0
        self.headingOffset = 0
        
        self.numStepsWalked = 0
        self.prevNumStepsWalked = 0
        self.numStepsWalkedOffset = 0
    
    '''
    Updates the fields of `self`.
    
    @param dataPacket
           the data packet received from Mega
    @return False if the last node in `route` is cleared; else return True
    '''
    def update(self, dataPacket, isNavigationPaused):
        global IS_SNAP_TO_GRAPH_EDGE, STEP_LENGTH, NODE_REACHED_THRESHOLD
        
        # to calculate `currHeading`
        self.initialHeading = dataPacket.initialHeading
        self.currHeading = (self.initialHeading + (dataPacket.numRightTurns - dataPacket.numLeftTurns) * 45) % 360
        self.currHeading = (self.currHeading + self.headingOffset) % 360
        
        # to update `currLocation`
        if isNavigationPaused == True:
            self.numStepsWalkedOffset += self.numStepsWalked - self.prevNumStepsWalked
        else:
            print('Updating `currLocation!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('currHeading = ' + str(self.currHeading))
            self.numStepsWalked = dataPacket.numStepsWalked
            deltaNumStepsWalked = self.numStepsWalked - self.prevNumStepsWalked + self.numStepsWalkedOffset
            deltaLocation = [0, 0]
            if self.currHeading > 22.5 and self.currHeading <= 67.5:
                deltaLocation[1] += STEP_LENGTH * deltaNumStepsWalked
            elif self.currHeading > 67.5 and self.currHeading <= 112.5:
                deltaLocation[0] += STEP_LENGTH * deltaNumStepsWalked / math.sqrt(2)
                deltaLocation[1] += STEP_LENGTH * deltaNumStepsWalked / math.sqrt(2)
            elif self.currHeading > 112.5 and self.currHeading <= 157.5:
                deltaLocation[0] += STEP_LENGTH * deltaNumStepsWalked
            elif self.currHeading > 157.5 and self.currHeading <= 202.5:
                deltaLocation[0] += STEP_LENGTH * deltaNumStepsWalked / math.sqrt(2)
                deltaLocation[1] -= STEP_LENGTH * deltaNumStepsWalked / math.sqrt(2)
            elif self.currHeading > 202.5 and self.currHeading <= 247.5:
                deltaLocation[1] -= STEP_LENGTH * deltaNumStepsWalked
            elif self.currHeading > 247.5 and self.currHeading <= 292.5:
                deltaLocation[0] -= STEP_LENGTH * deltaNumStepsWalked / math.sqrt(2)
                deltaLocation[1] -= STEP_LENGTH * deltaNumStepsWalked / math.sqrt(2)
            elif self.currHeading > 292.5 and self.currHeading <= 337.5:
                deltaLocation[0] -= STEP_LENGTH * deltaNumStepsWalked
            elif self.currHeading > 337.5 or self.currHeading <= 22.5:
                deltaLocation[0] -= STEP_LENGTH * deltaNumStepsWalked / math.sqrt(2)
                deltaLocation[1] += STEP_LENGTH * deltaNumStepsWalked / math.sqrt(2)
            self.currLocation[0] += deltaLocation[0]
            self.currLocation[1] += deltaLocation[1]
        
        # if inter-building, do teleportation
        if self.myMap.getNode(self.route[self.clearedRouteIdx]).nodeId == 1231 and \
                self.myMap.getNode(self.route[self.clearedRouteIdx + 1]).nodeId == 2201:
            print('Teleporting from COM1 to COM2!!!!!!!!!!!!!!')
            self.currLocation[0] = 61
            self.currLocation[1] = 4024
        elif self.myMap.getNode(self.route[self.clearedRouteIdx]).nodeId == 2201 and \
                self.myMap.getNode(self.route[self.clearedRouteIdx + 1]).nodeId == 1231:
            print('Teleporting from COM2 to COM1!!!!!!!!!!!!!!')
            self.currLocation[0] = 11815
            self.currLocation[1] = 406
        
        # if current location is within `NODE_REACHED_THRESHOLD` of the next node in `route`, then increment `clearedRouteIdx`
        if algorithms.computeDistance(self.currLocation,
                self.myMap.getNode(self.route[self.clearedRouteIdx + 1]).location) < NODE_REACHED_THRESHOLD:
            self.clearedRouteIdx = self.clearedRouteIdx + 1
            print(stringHelper.AUDIO + ' Reached node Id: #' + str(self.route[self.clearedRouteIdx]))
            audioOutput.playAudio('reachedNewNode_soundEffect')
            audioOutput.playAudio('reached')
            audioOutput.playInt(self.route[self.clearedRouteIdx])
            audioOutput.playAudio('node' + str(self.route[self.clearedRouteIdx]) + '_description')
            
            if self.myMap.getNode(self.route[self.clearedRouteIdx]).nodeId == 2214 or \
                    self.myMap.getNode(self.route[self.clearedRouteIdx]).nodeId == 1230:
                print(stringHelper.AUDIO + ' Climb stairs.')
                audioOutput.playAudio('climbStairs')
        
        # if the last node is cleared then return False
        if self.clearedRouteIdx == len(self.route) - 1:
            print(stringHelper.AUDIO + ' Navigation completed.')
            audioOutput.playAudio('navigationCompleted')
            return False
        
        # to calculate `expectedHeading`
        if self.myMap.getNode(self.route[self.clearedRouteIdx]).nodeId == 2201 and \
                self.myMap.getNode(self.route[self.clearedRouteIdx + 1]).nodeId == 2217:
            self.expectedHeading = algorithms.computeBearing(
                    self.myMap.getNode(1229).location,
                    self.myMap.getNode(1231).location
                    ) + 45 # @author chen-zhuo warning: hard-coded offset; assumes `northAt` is 315 for all maps
        elif self.myMap.getNode(self.route[self.clearedRouteIdx]).nodeId == 1231 and \
                self.myMap.getNode(self.route[self.clearedRouteIdx + 1]).nodeId == 1229:
            self.expectedHeading = algorithms.computeBearing(
                    self.myMap.getNode(2217).location,
                    self.myMap.getNode(2201).location
                    ) + 45 # @author chen-zhuo warning: hard-coded offset; assumes `northAt` is 315 for all maps
        else:
            self.expectedHeading = algorithms.computeBearing(
                    self.myMap.getNode(self.route[self.clearedRouteIdx]).location,
                    self.myMap.getNode(self.route[self.clearedRouteIdx + 1]).location
                    ) + 45 # @author chen-zhuo warning: hard-coded offset; assumes `northAt` is 315 for all maps
        
        # if `IS_SNAP_TO_GRAPH_EDGE` is True, do offset accordingly
        if IS_SNAP_TO_GRAPH_EDGE:
            if self.myMap.nodesDict[self.route[self.clearedRouteIdx]].location[0] == \
                    self.myMap.nodesDict[self.route[self.clearedRouteIdx + 1]].location[0]:
                self.currLocation[0] = self.myMap.nodesDict[self.route[self.clearedRouteIdx]].location[0]
            elif self.myMap.nodesDict[self.route[self.clearedRouteIdx]].location[1] == \
                    self.myMap.nodesDict[self.route[self.clearedRouteIdx + 1]].location[1]:
                self.currLocation[1] = self.myMap.nodesDict[self.route[self.clearedRouteIdx]].location[1]
        
#         print(stringHelper.INFO + ' Delta Location:   \x1b[1;31m(' +
#               str(deltaLocation[0]) + ', ' + str(deltaLocation[1]) + ')\x1b[0m')
        print(stringHelper.INFO + ' ' + stringHelper.highlight(' Current Location:  ') + ' (' +
              str(self.currLocation[0]) + ', ' + str(self.currLocation[1]) + ')')
        
        # to calculate `distanceUntilNextNode`
        self.distanceUntilNextNode = algorithms.computeDistance(self.currLocation,
                self.myMap.getNode(self.route[self.clearedRouteIdx + 1]).location)
        
        # to prepare 'previous' values before this function is called again
        self.prevNumStepsWalked = self.numStepsWalked
#         self.prevHeading = self.currHeading
        
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
