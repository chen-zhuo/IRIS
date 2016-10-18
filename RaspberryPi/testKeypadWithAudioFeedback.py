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
    
    userInput = None
    while userInput == None:
        userInput = keypadInput.getKeyPressesUntilHashKey()
    
    audioOutput.playAudio('youHaveKeyedIn')
    audioOutput.playAudio(userInput)
    audioOutput.playAudio('pressTheHashKeyToConfirmOrAsteriskKeyToReenter')
    isUserInputConfirmed = None
    while isUserInputConfirmed != '*' and isUserInputConfirmed != '#':
        isUserInputConfirmed = keypadInput.getKeyPress()
    if isUserInputConfirmed == '#':
        print('Comfirmed user input: ' + userInput)
        break
    else:
        continue

def playNum(num):
    while num > 0:
        digit = num % 10
        num /= 10
        audioOutput.playAudio(digit)

if __name__ == '__main__':
    _test()