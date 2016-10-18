'''
This is a unit-test file for keypad with audio feedback.

@author: chen-zhuo
'''

import algorithms
import audioOutput
import keypadInput
from time import sleep

def _test():
    keypadInput.initKeypad()
    audioOutput.initAudio()
    
    audioOutput.playAudio('welcomeToIris')
    sleep(1)
    audioOutput.playAudio('plsKeyInDestinationNodeIdFollowedByTheHashKey')
    
    while True:
        userInput = None
        while userInput == None:
            userInput = keypadInput.getKeyPressesUntilHashKey()
        
        audioOutput.playAudio('youHaveKeyedIn')
        playNum(userInput)
        audioOutput.playAudio('pressTheHashKeyToConfirmOrAsteriskKeyToReenter')
        isUserInputConfirmed = None
        while isUserInputConfirmed != '*' and isUserInputConfirmed != '#':
            isUserInputConfirmed = keypadInput.getKeyPress()
        if isUserInputConfirmed == '#':
            print('Comfirmed user input: ' + userInput)
            break
        else:
            continue
    
    keypadInput.closeKeypadThread()
    audioOutput.closeAudioThread()

def playNum(num):
    for i in range(len(num)):
        audioOutput.playAudio(num[i])

if __name__ == '__main__':
    _test()
