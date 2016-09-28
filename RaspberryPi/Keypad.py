'''
This file contains the definition of a 4 by 3 'Keypad' object class.

@author: chen-zhuo
'''

import datetime
import RPi.GPIO as GPIO # @UnresolvedImport

class Keypad():
    def __init__(self, keyRepeat = 0.1, delayUntilRepeat = 1):
        self.KEY_VALUES = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9'], ['*', '0', '#']]
        self.ROW = [7, 8, 25, 24] # raspberry pi pin numbers which are connected to the first 4 female connectors of
                                  # the keypad
        self.COLUMN = [11, 9, 10] # raspberry pi pin numbers which are connected to the last 3 female connectors of the
                                  # keypad
        
        self.keyRepeat = keyRepeat # time delay between successive key pressed events when a key is held
        self.delayUntilRepeat = delayUntilRepeat # time delay before registering successive key pressed events when a key is held
        self.prevKeyPressed = None
        self.isKeyBeingHeld = False
        self.prevTimestamp = None # updates when a key pressed event happens (incl. 'None' key pressed event); does not
                                  # update for subsequent same key pressed events
        self.prevTimestamp2 = None # updates when a successive same key pressed event is registered
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarning(False)
    
    def getKey(self):
        # to set all column GPIO pins as output low
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.OUT)
            GPIO.output(self.COLUMN[j], GPIO.LOW)
        
        # to set all row GPIO pins as input
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)
        
        # to scan rows for pressed key; a valid key press should set "rowVal"  between 0 and 3
        rowVal = -1
        for i in range(len(self.ROW)):
            tmpRead = GPIO.input(self.ROW[i])
            if tmpRead == 0:
                rowVal = i
        
        # if 'rowVal' is not 0 thru 3 then no button was pressed and we can exit
        if rowVal < 0 or rowVal > 3:
            self.exit()
            self.prevKeyPressed = None
            self.isKeyBeingHeld = False
            self.prevTimestamp = datetime.datetime.now()
            self.prevTimestamp2 = None
            return
        
        # to convert column GPIO pins to input
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        
        # to switch the 'i'-th row found from scan to output high
        GPIO.setup(self.ROW[rowVal], GPIO.OUT)
        GPIO.output(self.ROW[rowVal], GPIO.HIGH)
        
        # to scan columns for the pressed key; a valid key press should set 'colVal' between 0 and 2
        colVal = -1
        for j in range(len(self.COLUMN)):
            tmpRead = GPIO.input(self.COLUMN[j])
            if tmpRead == 1:
                colVal = j
        
        # if 'colVal' is not 0 thru 2 then no button was pressed and we can exit
        if colVal < 0 or colVal > 2:
            self.exit()
            self.prevKeyPressed = None
            self.isKeyBeingHeld = False
            self.prevTimestamp = datetime.datetime.now()
            self.prevTimestamp2 = None
            return
        
        # return the value of the key pressed
        keyPressed = self.KEY_VALUES[rowVal][colVal]
        self.exit()
        timestamp = datetime.datetime.now()
        
        if self.prevTimestamp == None or keyPressed != self.prevKeyPressed: # if a different key pressed event happens
            self.prevKeyPressed = keyPressed
            self.isKeyBeingHeld = False
            self.prevTimestamp = datetime.datetime.now()
            self.prevTimestamp2 = None
            return keyPressed
        elif keyPressed == self.prevKeyPressed and self.isKeyBeingHeld == False: # if the same key pressed event happens
                                                                               # for the second time
            self.isKeyBeingHeld = True
            return None
        elif keyPressed == self.prevKeyPressed and self.isKeyBeingHeld == True: # if the same key pressed event happens
                                                                                # for the third or subsequent time
            if timestamp - self.prevTimestamp < datetime.timedelta(seconds = self.delayUntilRepeat):
                return None
            elif self.prevTimestamp2 == None:
                self.prevTimestamp2 = datetime.datetime.now()
                return keyPressed
            elif timestamp - self.prevTimestamp2 < datetime.timedelta(seconds = self.keyRepeat):
                return None
            else:
                self.prevTimestamp2 = datetime.datetime.now()
                return keyPressed
    
    '''
    to re-initialize all rows and columns as input at exit
    '''
    def exit(self):
        for i in range(len(self.ROW)):
            GPIO.setup(self.ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP) 
        for j in range(len(self.COLUMN)):
            GPIO.setup(self.COLUMN[j], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    

def testKeypad():
    myKeypad = Keypad()
    keyPressed = None
    while True:
        keyPressed = myKeypad.getKey()
        if keyPressed == '#':
            print('#')
        elif keyPressed != None:
            print(keyPressed, end = "")

if __name__ == '__main__':
    testKeypad()
