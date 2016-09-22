// ---------------------------------------------------------------------------
// Example NewPing library sketch that does a ping about 20 times per second.
// ---------------------------------------------------------------------------

#include <NewPing.h>

#define TRIGGER_PIN  8  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     7  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 200 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

int distance;
int steps = 100;
int leftSensor = 200;
int rightSensor = 300;

int checkSum = 0;
int values[5]; // array size = 5

void setup() {
  Serial.begin(9600); // Open serial monitor at 115200 baud to see ping results.
  Serial1.begin(9600);
}

void updateSensor() {
  distance = sonar.ping_cm(); 
 // Serial.print("Distance:");
 // Serial.println(distance);
  delay(1000); // delay is needed to get a more accurate measurement for distance
}


void loop() {
  
  updateSensor();
  
  //Poll command sent from pi
  if(Serial1.available()) {
    int inByte = Serial1.read();
   
    if(inByte == 'H') { // HELLO
       Serial.println('H');
       Serial1.print('A'); 
    }

    if(inByte == 'A') { // Acknowledge
      Serial.println('A');
      Serial.println("Pi is ready"); 
    }

     if(inByte == 'P') {
      Serial.println(distance);
      values[0] = distance;
      values[1] = steps;
      values[2] = leftSensor;
      values[3] = rightSensor;

      // DEUGGING
      Serial.println(distance);
      Serial.println(steps);
      Serial.println(leftSensor);
      Serial.println(rightSensor);
      
      for(int i=0; i<4; i++) {
        checkSum += values[i];
        Serial1.println(values[i]);
      }
      
      values[4] = checkSum;
      Serial1.println(values[4]);
      Serial.print("CheckSum:");
      Serial.println(checkSum);
      checkSum = 0;
    }

  }

}
