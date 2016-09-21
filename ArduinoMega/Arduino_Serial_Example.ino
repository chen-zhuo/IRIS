/*
Mega multple serial test
Receives from the main serial port, sends to the others. Receives from serial port 1, sends to the main serial (Serial 0).
This example works only on the Arduino Mega
The circuit:
* Any serial device attached to Serial port 1 * Serial monitor open on Serial port 0:
created 30 Dec. 2008 modified 20 May 2012
by Tom Igoe & Jed Roach
This example code is in the public domain. */

void startup() {
  // put your main code here, to run repeatedly:
  // read from port 1, send to port 0:
  if (Serial1.available()) {
    int inByte = Serial1.read();
    if(inByte=='H') { // recieved hello
      Serial.print('H'); // send ack
      Serial1.print('A');
    //  Serial.print('\r');
    }

    else if(inByte == 'A'){ // recieve ack
      Serial.print('A');
      Serial1.print('R');
    //  Serial.print('\r');
    }

    else {
     Serial.println("nothing");
    }
    //Serial.write(inByte); 
    }
    
  // read from port 0, send to port 1: // is this working?
  if (Serial.available()) {
    int inByte = Serial.read(); 
      if(inByte=='H') { // recieved hello
      //Serial1.print('A'); // send ack
     // Serial1.print('\r');
    }

    else if(inByte == 'A'){ // recieve ack
      //Serial1.print('R');
     // Serial1.print('\r');
    }
    
  }
}

void setup() {
  // initialize both serial ports
  Serial.begin(9600);
  Serial1.begin(9600);
}

void loop() {
  startup();
}

