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
    global isAudioInitted, audioDict
    
    if isAudioInitted == False:
        initAudio()
    
    try:
        os.system('mpg123 -q ' + audioDict[audioName] + ' &')
    except KeyError:
        print('Error when calling audio.playAudioNow(): The audio file with name ' + audioName + ' does not exist.')

'''
Enqueues an .mp3 audio file for playback over the earphone. Waits for current audio files to finish playing (if any)
before playing this audio file.

@param audioName
           the description of the audio; e.g. 'turnLeft', 'plsKeyInDestinationNodeIdFollowedByTheHashKey'
'''
def playAudio(audioName):
    global isAudioInitted, audioQueue, audioDict
    
    if isAudioInitted == False:
        initAudio()
    
    try:
        audioQueue.append(audioDict[audioName])
    except KeyError:
        print(stringHelper.ERROR + ' at audio.playAudio(): The audio file with name ' + audioName + ' does not exist.')

def playInt(num):
    num = int(num)
    if str(num)[0] == '-':
        playAudio('negative')
        num = str(num)[1:]
    for i in range(len(str(num))):
        playAudio(str(num)[i])

'''
Defines `playAudioQueueThread` which is started by `initAudio()`.
'''
def _playAudioQueue():
    global audioQueue, isAudioThreadActive
    
    print(stringHelper.MESSAGE + ' `playAudioQueueThread` started.')
    
    isAudioThreadActive = True
    
    while isAudioThreadActive:
        if len(audioQueue) > 0:
            nextAudioFileInQueue = audioQueue[0]
            audioQueue.pop(0)
            os.system('mpg123 -q ' + nextAudioFileInQueue)
    
    print(stringHelper.MESSAGE + ' `playAudioQueueThread` closed.')

'''
Initializes `audioDict` and starts `playAudioQueueThread`. Remember to call `closeAudioThread()` when finished.
'''
def initAudio():
    global isAudioInitted, audioQueue, audioDict, audioTextDict
    
    isAudioInitted = True
    
    # ======================================== BEGIN AUDIO FILES LIST ========================================
    
    # welcome sounds and interactive node ID key-in
    audioDict['welcomeToIris'] = './AudioFiles/welcomeToIris.mp3'
    audioDict['arpeggio_soundEffect'] = './AudioFiles/arpeggio_soundEffect.mp3'
#     audioDict['plsKeyInOriginBuildingIdFollowedByTheHashKey'] = './AudioFiles/plsKeyInOriginBuildingIdFollowedByTheHashKey.mp3'
#     audioDict['plsKeyInOriginBuildingStoreyFollowedByTheHashKey'] = './AudioFiles/plsKeyInOriginBuildingStoreyFollowedByTheHashKey.mp3'
    audioDict['plsKeyInOriginNodeIdFollowedByTheHashKey'] = './AudioFiles/plsKeyInOriginNodeIdFollowedByTheHashKey.mp3'
#     audioDict['plsKeyInDestinationBuildingIdFollowedByTheHashKey'] = './AudioFiles/plsKeyInDestinationBuildingIdFollowedByTheHashKey.mp3'
#     audioDict['plsKeyInDestinationBuildingStoreyFollowedByTheHashKey'] = './AudioFiles/plsKeyInDestinationBuildingStoreyFollowedByTheHashKey.mp3'
    audioDict['plsKeyInDestinationNodeIdFollowedByTheHashKey'] = './AudioFiles/plsKeyInDestinationNodeIdFollowedByTheHashKey.mp3'
    audioDict['youHaveKeyedIn'] = './AudioFiles/youHaveKeyedIn.mp3'
    audioDict['pressTheHashKeyToConfirmOrAsteriskKeyToReenter'] = './AudioFiles/pressTheHashKeyToConfirmOrAsteriskKeyToReenter.mp3'
    audioDict['confirmed'] = './AudioFiles/confirmed.mp3'
    audioDict['navigationStarted'] = './AudioFiles/navigationStarted.mp3'
    
    # sound effects and tones
    audioDict['beep'] = './AudioFiles/beep.mp3'
    audioDict['heading+0_soundEffect'] = './AudioFiles/heading+0_soundEffect.mp3'
    audioDict['heading-45_soundEffect'] = './AudioFiles/heading-45_soundEffect.mp3'
    audioDict['heading+45_soundEffect'] = './AudioFiles/heading+45_soundEffect.mp3'
    audioDict['heading-90_soundEffect'] = './AudioFiles/heading-90_soundEffect.mp3'
    audioDict['heading+90_soundEffect'] = './AudioFiles/heading+90_soundEffect.mp3'
    audioDict['heading-135_soundEffect'] = './AudioFiles/heading-135_soundEffect.mp3'
    audioDict['heading+135_soundEffect'] = './AudioFiles/heading+135_soundEffect.mp3'
    audioDict['heading+180_soundEffect'] = './AudioFiles/heading+180_soundEffect.mp3'
    audioDict['reachedNewNode_soundEffect'] = './AudioFiles/reachedNewNode_soundEffect.mp3'
    
    # keypad key names
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
    
    # when user keys in '1', snap to the previous node
    audioDict['snappedToPrevNode'] = './AudioFiles/snappedToPrevNode.mp3'
    
    # when user keys in '3', snap to the next node
    audioDict['snappedToNextNode'] = './AudioFiles/snappedToNextNode.mp3'
    
    # when user keys in '5', force correct heading
    audioDict['forcedCorrectHeading'] = './AudioFiles/forcedCorrectHeading.mp3'
    
    # when user keys in '9', give detailed audio feedback, e.g. "from 1201 towards 1202 then {go straight ||
    # turn left || turn right || climb stairs || navigation completed}, steps remaining: 10"
    audioDict['from'] = './AudioFiles/from.mp3'
    audioDict['towards'] = './AudioFiles/towards.mp3'
    audioDict['then'] = './AudioFiles/then.mp3'
    audioDict['goStraight'] = './AudioFiles/goStraight.mp3'
    audioDict['turnLeft'] = './AudioFiles/turnLeft.mp3'
    audioDict['turnRight'] = './AudioFiles/turnRight.mp3'
    audioDict['climbStairs'] = './AudioFiles/climbStairs.mp3'
    audioDict['navigationCompleted'] = './AudioFiles/navigationCompleted.mp3'
    audioDict['stepsRemaining'] = './AudioFiles/stepsRemaining.mp3'
    
    # when user keys in '0', pause/resume step counting
    audioDict['pausingStepCounting'] = './AudioFiles/pausingStepCounting.mp3'
    audioDict['resumingStepCounting'] = './AudioFiles/resumingStepCounting.mp3'
    
    # audio feedback when user reach a node
    audioDict['reached'] = './AudioFiles/reached.mp3'
    audioDict['numberOfStairsExpected'] = './AudioFiles/numberOfStairsExpected.mp3'
    audioDict['plsPress3WhenFinishedClimbing'] = './AudioFiles/plsPress3WhenFinishedClimbing.mp3'
    
    # node descriptions
    audioDict['node1201_description'] = './AudioFiles/node1201_description.mp3'
    # TODO by @author beiyu
    
    # miscellaneous
    audioDict['negative'] = './AudioFiles/negative.mp3'
    
    # ======================================== END AUDIO FILES LIST ========================================
    
    # to map `audioName` to its description
#     audioTextDict['plsKeyInOriginBuildingIdFollowedByTheHashKey'] = 'Please key in origin building ID, followed by the hash key.'
#     audioTextDict['plsKeyInOriginBuildingStoreyFollowedByTheHashKey'] = 'Please key in origin building storey, followed by the hash key.'
    audioTextDict['plsKeyInOriginNodeIdFollowedByTheHashKey'] = 'Please key in origin node ID, followed by the hash key.'
#     audioTextDict['plsKeyInDestinationBuildingIdFollowedByTheHashKey'] = 'Please key in destination building ID, followed by the hash key.'
#     audioTextDict['plsKeyInDestinationBuildingStoreyFollowedByTheHashKey'] = 'Please key in destination building storey, followed by the hash key.'
    audioTextDict['plsKeyInDestinationNodeIdFollowedByTheHashKey'] = 'Please key in destination node ID, followed by the hash key.'
    
    # to start `playAudioQueueThread`
    audioQueue = []
    playAudioQueueThread = Thread(target=_playAudioQueue)
    playAudioQueueThread.start()

'''
Closes `playAudioQueueThread`.
'''
def closeAudioThread():
    global isAudioThreadActive, audioQueue
    
    while audioQueue != []:
        sleep(1)
    isAudioThreadActive = False

def _test():
    initAudio()
    
    print(stringHelper.AUDIO + ' Welcome to IRIS.')
    playAudio('welcomeToIris')
    print(stringHelper.AUDIO + ' Playing arpeggio audio test...')
    playAudio('arpeggio_soundEffect')
    sleep(9)
    
    print(stringHelper.MESSAGE + ' Playing audio files simultaneously...')
    sleep(1)
    print(stringHelper.AUDIO + ' Go straight.')
    playAudioNow('goStraight')
    print(stringHelper.AUDIO + ' Turn left.')
    playAudioNow('turnLeft')
    print(stringHelper.AUDIO + ' Turn right.')
    playAudioNow('turnRight')
    sleep(2)
    
    print(stringHelper.MESSAGE + ' Playing audio files one after another...')
    sleep(1)
    print(stringHelper.AUDIO + ' Go straight.')
    playAudio('goStraight')
    print(stringHelper.AUDIO + ' Turn left.')
    playAudio('turnLeft')
    print(stringHelper.AUDIO + ' Turn right.')
    playAudio('turnRight')
    
    closeAudioThread()

if __name__ == '__main__':
    _test()
