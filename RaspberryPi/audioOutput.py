'''
This file contains algorithms related to audio output. During navigation, the user receives audio feedback (turn-by-turn
navigation information) over the earphone.

@author: chen-zhuo
'''

from threading import Thread
from time import sleep

import os

audioDict = {} # to map 'audioName' (key) to the corresponding file name with path (value)
audioQueue = [] # a queue of audio file names (with paths) to be played one after another
isAudioInitted = False
isAudioThreadActive = False

'''
Immediately plays an .mp3 audio file over the earphone. If there is already an audio file being played, they will be
played simultaneously.

@param audioName
           the description of the audio; e.g. 'turnLeft', 'plsKeyInDestinationNodeIdFollowedByTheHashKey'
'''
def playAudioNow(audioName):
    if isAudioInitted == False:
        initAudio()
    
    if audioDict[audioName] != None:
        os.system('mpg123 -q ' + audioDict[audioName] + ' &')
    else:
        print('Error when calling audio.playAudioNow(): The audio file with name ' + audioName + ' does not exist.')

'''
Enqueues an .mp3 audio file for playback over the earphone. Waits for current audio files to finish playing (if any)
before playing this audio file.

@param audioName
           the description of the audio; e.g. 'turnLeft', 'plsKeyInDestinationNodeIdFollowedByTheHashKey'
'''
def playAudio(audioName):
    if isAudioInitted == False:
        initAudio()
    
    if audioDict[audioName] != None:
        audioQueue.append(audioDict[audioName])
    else:
        print('Error when calling audio.playAudio(): The audio file with name ' + audioName + ' does not exist.')

'''
Defines 'playAudioQueueThread' which is started by 'initAudio()'.
'''
def playAudioQueue():
    print('\'playAudioQueueThread\' is starting...')
    
    global isAudioThreadActive, audioQueue
    isAudioThreadActive = True
    
    while isAudioThreadActive:
        if len(audioQueue) > 0:
            nextAudioFileInQueue = audioQueue[0]
            audioQueue.pop(0)
            os.system('mpg123 -q ' + nextAudioFileInQueue)
    
    print('\'playAudioQueueThread\' is closing...')

'''
Initializes 'audioDict' and starts 'playAudioQueueThread'.
'''
def initAudio():
#     global isAudioInitted
    
    audioDict['null'] = './AudioFiles/null.mp3' # a short, blank audio file
    
    audioDict['welcomeToIris'] = './AudioFiles/welcomeToIris.mp3'
    audioDict['plsKeyInOriginBuildingIdFollowedByTheHashKey'] = './AudioFiles/plsKeyInOriginBuildingIdFollowedByTheHashKey.mp3'
    audioDict['plsKeyInOriginBuildingStoreyFollowedByTheHashKey'] = './AudioFiles/plsKeyInOriginBuildingStoreyFollowedByTheHashKey.mp3'
    audioDict['plsKeyInOriginNodeIdFollowedByTheHashKey'] = './AudioFiles/plsKeyInOriginNodeIdFollowedByTheHashKey.mp3'
    audioDict['plsKeyInDestinationBuildingIdFollowedByTheHashKey'] = './AudioFiles/plsKeyInDestinationBuildingIdFollowedByTheHashKey.mp3'
    audioDict['plsKeyInDestinationBuildingStoreyFollowedByTheHashKey'] = './AudioFiles/plsKeyInDestinationBuildingStoreyFollowedByTheHashKey.mp3'
    audioDict['plsKeyInDestinationNodeIdFollowedByTheHashKey'] = './AudioFiles/plsKeyInDestinationNodeIdFollowedByTheHashKey.mp3'
    audioDict['youHaveKeyedIn'] = './AudioFiles/youHaveKeyedIn.mp3'
    audioDict['pressTheHashKeyToConfirmOrAsteriskKeyToReenter'] = './AudioFiles/pressTheHashKeyToConfirmOrAsteriskKeyToReenter.mp3'
    audioDict['confirmed'] = './AudioFiles/confirmed.mp3'
    
#     audioDict['navigationStarted'] = './AudioFiles/navigationStarted.mp3'
#     audioDict['navigationCompleted'] = './AudioFiles/navigationCompleted.mp3'
#     audioDict['nextNodeId'] = './AudioFiles/nextNodeId.mp3'
#     audioDict['reachedNodeId'] = './AudioFiles/reachedNodeId.mp3'
#     audioDict['reachedDestinationNodeId'] = './AudioFiles/reachedDestinationNodeId.mp3'
#     audioDict['enteredBuilding'] = './AudioFiles/enteredBuilding.mp3'
#     audioDict['com1'] = './AudioFiles/com1.mp3'
#     audioDict['com2'] = './AudioFiles/com2.mp3'
#     audioDict['upwardStaircaseAhead'] = './AudioFiles/upwardStaircaseAhead.mp3' # downward staircase is not examinable
#     audioDict['numberOfStairsExpected'] = './AudioFiles/numberOfStairsExpected.mp3'
#     audioDict['reachedStorey'] = './AudioFiles/reachedStorey.mp3'
    
    audioDict['goStraight'] = './AudioFiles/goStraight.mp3'
    audioDict['turnLeft'] = './AudioFiles/turnLeft.mp3'
    audioDict['turnRight'] = './AudioFiles/turnRight.mp3'
    audioDict['adjustYourBearingSlightlyToTheLeft'] = './AudioFiles/adjustYourBearingSlightlyToTheLeft.mp3'
    audioDict['adjustYourBearingSlightlyToTheRight'] = './AudioFiles/adjustYourBearingSlightlyToTheRight.mp3'
    
    audioDict['zero'] = './AudioFiles/zero.mp3'
    audioDict['one'] = './AudioFiles/one.mp3'
    audioDict['two'] = './AudioFiles/two.mp3'
    audioDict['three'] = './AudioFiles/three.mp3'
    audioDict['four'] = './AudioFiles/four.mp3'
    audioDict['five'] = './AudioFiles/five.mp3'
    audioDict['six'] = './AudioFiles/six.mp3'
    audioDict['seven'] = './AudioFiles/seven.mp3'
    audioDict['eight'] = './AudioFiles/eight.mp3'
    audioDict['nine'] = './AudioFiles/nine.mp3'
    audioDict['asterisk'] = './AudioFiles/asterisk.mp3'
    audioDict['hash'] = './AudioFiles/hash.mp3'
    
    # to start 'playAudioQueueThread'
    audioQueue = []
    playAudioQueueThread = Thread(target = playAudioQueue)
    playAudioQueueThread.start()
    playAudio(audioDict['null'])
    
    isAudioInitted = True

'''
Closes 'playAudioQueueThread'.
'''
def closeAudioThread():
    global isAudioThreadActive
    isAudioThreadActive = False

def testAudio():
    print('Starting audio test...')
    
    print('Initializing audio...')
    initAudio()
    
    print('Playing welcome audio...')
    playAudioNow('welcomeToIris')
    sleep(5)
    
    print('Playing multiple audio files simultaneously...')
    playAudioNow('goStraight')
    playAudioNow('turnLeft')
    playAudioNow('turnRight')
    playAudioNow('adjustYourBearingSlightlyToTheLeft')
    playAudioNow('adjustYourBearingSlightlyToTheRight')
    sleep(7)
    
    print('Playing multiple audio files one after another...')
    playAudio('goStraight')
    playAudio('turnLeft')
    playAudio('turnRight')
    playAudio('adjustYourBearingSlightlyToTheLeft')
    playAudio('adjustYourBearingSlightlyToTheRight')
    sleep(15)
    
    print('Closing audio...')
    closeAudioThread()

if __name__ == '__main__':
    testAudio()
