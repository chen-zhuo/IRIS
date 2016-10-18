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
        
        print('You have keyed in: ' + userInput)
        print('Press the hash key to confirm, or asterisk key to re-enter.')
        isUserInputConfirmed = None
        while isUserInputConfirmed != '*' and isUserInputConfirmed != '#':
            isUserInputConfirmed = keypadInput.getKeyPress()
        if isUserInputConfirmed == '#':
            print('Comfirmed user input: ' + userInput)
            break
        else:
            continue
    

if __name__ == '__main__':
    _test()