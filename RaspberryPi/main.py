'''
This file contains the `main()` function, which is the starting point of the program. High-level algorithms such as task
scheduling, thread instantiations, are defined here.

@author: chen-zhuo
'''

from algorithms import computeRoute, downloadAndParseMap, linkMaps, printWelcomeMsg
from audio import initAudio, playAudio, playAudioNow
import json
from pprint import pprint
from threading import Thread
from time import sleep

def main():
    initAudio()
    
    printWelcomeMsg()
    playAudio('welcomeToIris')
    sleep(3)
    
    playAudio('plsKeyInOriginBuildingIdFollowedByTheHashKey')
#     srcBuildingId = 
    
    
if __name__ == '__main__':
    main()
