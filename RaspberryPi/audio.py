'''
This file contains algorithms related to audio output. During navigation, the user receives audio feedback (turn-by-turn
navigation information) over the earphone.

@author: chen-zhuo
'''

from threading import Thread
from time import sleep

import pygame # @UnresolvedImport
import random
from warnings import catch_warnings

isAudioInitted = False
audioDict = {} # to map 'audioName' (key) to the corresponding file name with path (value)
audioQueue = [] # a queue of audio files to be played one after another
mainChannel = None

# import pygame.mixer
# from pygame.mixer import Sound
# from threading import Thread
# import random
# 
# pygame.mixer.init()
# 
# #fileDir = '/home/pi/Documents/sound.mp3'
# 
# #turnR.play()
# 
# def playNum(fileDir):
#     if fileDir == '/home/pi/Documents/sound.mp3':
#         Thread(target = loadBGM).start()
#     else:
#         num = Sound(fileDir)
#         pygame.mixer.music.set_volume(0.5)
#         num.play()
# 
# musicList = ['sound.mp3']
# 
# def loadBGM():
#     bgm = random.choice(musicList)
#     pygame.mixer.music.set_volume(0.9)
# 
#     pygame.mixer.music.load('/home/pi/Documents/sound.mp3')
#     playBGM()
# 
# def playBGM():
#     pygame.mixer.music.play()
# 
# #while the user is waiting
# #def playMusic():
# #Thread(target = loadBGM).start()
# Thread(target = playNum(fileDir)).start()
# print "music end"

def playAudio(audioName):
    if not isAudioInitted:
        init()
    
    if audioDict[audioName] != None:
        mainChannel.play(audioDict[audioName])
    else:
        print('ERROR: The audio file with name ' + audioName + ' does not exist.')

def init():
    pygame.init()
    pygame.mixer.init()
    
#     audioDict['beep'] = pygame.mixer.Sound('./AudioFiles/beep.wav')
#     audioDict['welcomeToIris'] = pygame.mixer.Sound('./AudioFiles/welcomeToIris.wav')
#     audioDict['plsKeyInOriginBuildingIdFollowedByThePoundKey'] = pygame.mixer.Sound('./AudioFiles/plsKeyInOriginBuildingIdFollowedByThePoundKey.wav')
#     audioDict['plsKeyInOriginStoreyFollowedByThePoundKey'] = pygame.mixer.Sound('./AudioFiles/plsKeyInOriginStoreyFollowedByThePoundKey.wav')
#     audioDict['plsKeyInOriginNodeIdFollowedByThePoundKey'] = pygame.mixer.Sound('./AudioFiles/plsKeyInOriginNodeIdFollowedByThePoundKey.wav')
#     audioDict['plsKeyInDestinationBuildingIdFollowedByThePoundKey'] = pygame.mixer.Sound('./AudioFiles/plsKeyInDestinationBuildingIdFollowedByThePoundKey.wav')
#     audioDict['plsKeyInDestinationStoreyFollowedByThePoundKey'] = pygame.mixer.Sound('./AudioFiles/plsKeyInDestinationStoreyFollowedByThePoundKey.wav')
#     audioDict['plsKeyInDestinationNodeIdFollowedByThePoundKey'] = pygame.mixer.Sound('./AudioFiles/plsKeyInDestinationNodeIdFollowedByThePoundKey.wav')
#     audioDict['youHaveKeyedIn'] = pygame.mixer.Sound('./AudioFiles/youHaveKeyedIn.wav')
#     audioDict['pressThePoundKeyToConfirmOrHashKeyToReenter'] = pygame.mixer.Sound('./AudioFiles/pressThePoundKeyToConfirmOrHashKeyToReenter.wav')
#     audioDict['confirmed'] = pygame.mixer.Sound('./AudioFiles/confirmed.wav')
#     audioDict['navigationStarted'] = pygame.mixer.Sound('./AudioFiles/navigationStarted.wav')
#     audioDict['navigationCompleted'] = pygame.mixer.Sound('./AudioFiles/navigationCompleted.wav')
#     audioDict['nextNodeId'] = pygame.mixer.Sound('./AudioFiles/nextNodeId.wav')
#     audioDict['reachedNodeId'] = pygame.mixer.Sound('./AudioFiles/reachedNodeId.wav')
#     audioDict['reachedDestinationNodeId'] = pygame.mixer.Sound('./AudioFiles/reachedDestinationNodeId.wav')
#     audioDict['enteredBuilding'] = pygame.mixer.Sound('./AudioFiles/enteredBuilding.wav')
#     audioDict['com1'] = pygame.mixer.Sound('./AudioFiles/com1.wav')
#     audioDict['com2'] = pygame.mixer.Sound('./AudioFiles/com2.wav')
#     audioDict['upwardStaircaseAhead'] = pygame.mixer.Sound('./AudioFiles/upwardStaircaseAhead.wav') # downward staircase is not examinable
#     audioDict['numberOfStairsExpected'] = pygame.mixer.Sound('./AudioFiles/numberOfStairsExpected.wav')
#     audioDict['reachedStorey'] = pygame.mixer.Sound('./AudioFiles/reachedStorey.wav')
#     
#     audioDict['goStraight'] = pygame.mixer.Sound('./AudioFiles/goStraight.wav')
#     audioDict['turnLeft'] = pygame.mixer.Sound('./AudioFiles/turnLeft.wav')
#     audioDict['turnRight'] = pygame.mixer.Sound('./AudioFiles/turnRight.wav')
#     audioDict['adjustBearingToTheLeft'] = pygame.mixer.Sound('./AudioFiles/adjustBearingToTheLeft.wav')
#     audioDict['adjustBearingToTheRight'] = pygame.mixer.Sound('./AudioFiles/adjustBearingToTheRight.wav')
#     
#     audioDict['zero'] = pygame.mixer.Sound('./AudioFiles/zero.wav')
#     audioDict['one'] = pygame.mixer.Sound('./AudioFiles/one.wav')
#     audioDict['two'] = pygame.mixer.Sound('./AudioFiles/two.wav')
#     audioDict['three'] = pygame.mixer.Sound('./AudioFiles/three.wav')
#     audioDict['four'] = pygame.mixer.Sound('./AudioFiles/four.wav')
#     audioDict['five'] = pygame.mixer.Sound('./AudioFiles/five.wav')
#     audioDict['six'] = pygame.mixer.Sound('./AudioFiles/six.wav')
#     audioDict['seven'] = pygame.mixer.Sound('./AudioFiles/seven.wav')
#     audioDict['eight'] = pygame.mixer.Sound('./AudioFiles/eight.wav')
#     audioDict['nine'] = pygame.mixer.Sound('./AudioFiles/nine.wav')
#     audioDict['hash'] = pygame.mixer.Sound('./AudioFiles/hash.wav')
#     audioDict['pound'] = pygame.mixer.Sound('./AudioFiles/pound.wav')
    
    mainChannel = pygame.mixer.Channel(1)
    mainChannel.set_volume(1.0)
    
    isAudioInitted = True

if __name__ == '__main__':
    init()
    mainChannel.play(pygame.mixer.Sound('./AudioFiles/welcomeToIris.mp3'))
