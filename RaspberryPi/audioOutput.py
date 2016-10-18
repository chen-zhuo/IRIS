'''
This file contains algorithms related to audio output. During navigation, the user receives audio feedback (turn-by-turn
navigation information) over the earphone.

@author: chen-zhuo
'''

import os
import stringHelper
from threading import Thread
from time import sleep

audioQueue = [] # a queue of audio file names (with paths) to be played one after another
audioDict = {} # to map `audioName` (key) to the corresponding file name with path (value)
audioTextDict = {} # to map `audioName` (key) to the corresponding text (value)
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
        print(stringHelper.AUDIO + '')
    else:
        print(stringHelper.ERROR + ' at audio.playAudio(): The audio file with name ' + audioName + ' does not exist.')

def playNum(num):
    for i in range(len(num)):
        playAudio(num[i])

'''
Defines `playAudioQueueThread` which is started by `initAudio()`.
'''
def _playAudioQueue():
    print(stringHelper.MESSAGE + ' `playAudioQueueThread` started.')
    
#     global isAudioThreadActive, audioQueue
    isAudioThreadActive = True
    
    while isAudioThreadActive:
        if len(audioQueue) > 0:
            nextAudioFileInQueue = audioQueue[0]
            audioQueue.pop(0)
            os.system('mpg123 -q ' + nextAudioFileInQueue)
    
    print(stringHelper.MESSAGE + ' `playAudioQueueThread` closed.')

'''
Initializes `audioDict` and starts `playAudioQueueThread`.
'''
def initAudio():
#     global isAudioInitted
    isAudioInitted = True
    
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
    
    audioDict['navigationStarted'] = './AudioFiles/navigationStarted.mp3'
    audioDict['navigationCompleted'] = './AudioFiles/navigationCompleted.mp3'
    audioDict['nextNodeIdIs'] = './AudioFiles/nextNodeIdIs.mp3'
    audioDict['reached'] = './AudioFiles/reached.mp3'
    audioDict['building'] = './AudioFiles/buildling.mp3'
    audioDict['storey'] = './AudioFiles/storey.mp3'
    audioDict['nodeId'] = './AudioFiles/nodeId.mp3'
    audioDict['com1'] = './AudioFiles/com1.mp3'
    audioDict['com2'] = './AudioFiles/com2.mp3'
    audioDict['upwardStaircaseAhead'] = './AudioFiles/upwardStaircaseAhead.mp3' # downward staircase is not examinable
    audioDict['numberOfStairsExpected'] = './AudioFiles/numberOfStairsExpected.mp3'
    
    audioDict['goStraight'] = './AudioFiles/goStraight.mp3'
    audioDict['turnLeft'] = './AudioFiles/turnLeft.mp3'
    audioDict['turnRight'] = './AudioFiles/turnRight.mp3'
    audioDict['adjustYourBearingSlightlyToTheLeft'] = './AudioFiles/adjustYourBearingSlightlyToTheLeft.mp3'
    audioDict['adjustYourBearingSlightlyToTheRight'] = './AudioFiles/adjustYourBearingSlightlyToTheRight.mp3'
    
    audioDict['0'] = './AudioFiles/0.mp3'
    audioDict['1'] = './AudioFiles/1.mp3'
    audioDict['2'] = './AudioFiles/2.mp3'
    audioDict['3'] = './AudioFiles/3.mp3'
    audioDict['4'] = './AudioFiles/4.mp3'
    audioDict['5'] = './AudioFiles/5.mp3'
    audioDict['6'] = './AudioFiles/6.mp3'
    audioDict['7'] = './AudioFiles/7.mp3'
    audioDict['8'] = './AudioFiles/8.mp3'
    audioDict['9'] = './AudioFiles/9.mp3'
    audioDict['asterisk'] = './AudioFiles/asterisk.mp3'
    audioDict['hash'] = './AudioFiles/hash.mp3'
    
    audioTextDict['welcomeToIris'] = 'Welcome to IRIS.'
    audioTextDict['plsKeyInOriginBuildingIdFollowedByTheHashKey'] = 'Please key in origin building ID, followed by the hash key.'
    audioTextDict['plsKeyInOriginBuildingStoreyFollowedByTheHashKey'] = 'Please key in origin building storey, followed by the hash key.'
    audioTextDict['plsKeyInOriginNodeIdFollowedByTheHashKey'] = 'Please key in origin building storey, followed by the hash key.'
    audioTextDict['plsKeyInDestinationBuildingIdFollowedByTheHashKey'] = 'Please key in destination building ID, followed by the hash key.'
    audioTextDict['plsKeyInDestinationBuildingStoreyFollowedByTheHashKey'] = 'Please key in destination building storey, followed by the hash key.'
    audioTextDict['plsKeyInDestinationNodeIdFollowedByTheHashKey'] = 'Please key in destination node ID, followed by the hash key.'
    audioTextDict['youHaveKeyedIn'] = 'You have keyed in'
    audioTextDict['pressTheHashKeyToConfirmOrAsteriskKeyToReenter'] = 'Press the hash key to confirm, or asterisk key to re-enter.'
    audioTextDict['confirmed'] = 'Comfirmed.'
    
    audioTextDict['navigationStarted'] = 'Navigation started.'
    audioTextDict['navigationCompleted'] = 'Navigation completed.'
    audioTextDict['nextNodeIdIs'] = 'Next node ID is'
    audioTextDict['reached'] = 'Reached'
    audioTextDict['building'] = 'building'
    audioTextDict['storey'] = 'storey'
    audioTextDict['nodeId'] = 'node ID'
    audioTextDict['com1'] = 'COM1'
    audioTextDict['com2'] = 'COM2'
    audioTextDict['upwardStaircaseAhead'] = 'Upward staircase ahead.'
    audioTextDict['numberOfStairsExpected'] = 'Number of Stairs expected'
    
    audioTextDict['goStraight'] = 'Go straight.'
    audioTextDict['turnLeft'] = 'Turn left.'
    audioTextDict['turnRight'] = 'Turn right.'
    audioTextDict['adjustYourBearingSlightlyToTheLeft'] = 'Adjust your bearing slightly to the left.'
    audioTextDict['adjustYourBearingSlightlyToTheRight'] = 'Adjust your bearing slightly to the right.'
    
    audioTextDict['0'] = 'zero'
    audioTextDict['1'] = 'one'
    audioTextDict['2'] = 'two'
    audioTextDict['3'] = 'three'
    audioTextDict['4'] = 'four'
    audioTextDict['5'] = 'five'
    audioTextDict['6'] = 'six'
    audioTextDict['7'] = 'seven'
    audioTextDict['8'] = 'eight'
    audioTextDict['9'] = 'nine'
    audioTextDict['asterisk'] = 'asterisk'
    audioTextDict['hash'] = 'hash'
    
    # to start `playAudioQueueThread`
    audioQueue = []
    playAudioQueueThread = Thread(target = _playAudioQueue)
    playAudioQueueThread.start()

'''
Closes `playAudioQueueThread`.
'''
def closeAudioThread():
#     global isAudioThreadActive, audioQueue
    
    while audioQueue != []:
        sleep(1)
    
    isAudioThreadActive = False

def _test():
    initAudio()
    
    print(stringHelper.MESSAGE + ' Playing welcome audio...')
    playAudioNow('welcomeToIris')
    sleep(3)
    
    print(stringHelper.MESSAGE + ' Playing multiple audio files simultaneously...')
    playAudioNow('goStraight')
    playAudioNow('turnLeft')
    playAudioNow('turnRight')
    playAudioNow('adjustYourBearingSlightlyToTheLeft')
    playAudioNow('adjustYourBearingSlightlyToTheRight')
    sleep(4)
    
    print(stringHelper.MESSAGE + ' Playing multiple audio files one after another...')
    playAudio('goStraight')
    playAudio('turnLeft')
    playAudio('turnRight')
    playAudio('adjustYourBearingSlightlyToTheLeft')
    playAudio('adjustYourBearingSlightlyToTheRight')
    sleep(9)
    
    print(stringHelper.MESSAGE + ' Closing audio...')
    sleep(1)
    closeAudioThread()

if __name__ == '__main__':
    _test()
