#include <NewPing.h>
#include <Wire.h>
#include <L3G.h>
#include <LSM303.h>

#define SONAR_NUM     3 // Number of sensors.
#define MAX_DISTANCE 300 // Maximum distance (in cm) to ping.
#define PING_INTERVAL 33 // Milliseconds between sensor pings (29ms is about the min to avoid cross-sensor echo).

#define TRIGGER_HAND  22
#define ECHO_HAND     23

#define TRIGGER_LEFT  24
#define ECHO_LEFT     25

#define TRIGGER_RIGHT  26
#define ECHO_RIGHT     27

//#define TRIGGER_FRONT  28
//#define ECHO_FRONT     29

#define VIBRATOR_HAND 2
#define VIBRATOR_LEFT 3
#define VIBRATOR_RIGHT 4


#define BUZZER 30

L3G gyro;
LSM303 compass;
LSM303::vector<int16_t> running_min = {32767, 32767, 32767}, running_max = { -32768, -32768, -32768};

// variables not passed to raspberry
int dc_offset_x = 0;
int dc_offset_y = 0;
int dc_offset_z = 0;
int prev_rate = 0;
int prev2_rate = 0;
int rate;
int sampleNum = 100;
int sampleTime = 10;
double angle = 0;
double noise = 0;
float heading;
unsigned long time;

int AN[3]; // array that stores the gyro data
int AN_OFFSET[3] = { -27, -27, -17}; //Array that stores the offset of the sensors
int SENSOR_SIGN[9] = {1, 1, 1, -1, -1, -1, 1, 1, 1}; // corrected directions x,y,z - gyro, accelerometer, magnetometer - words face up

// variables to be sent to raspberry
int gyro_x;
int gyro_y;
int gyro_z;
int steps = 0;
int left_turn = 0;
int right_turn = 0;
int left_ss = 0;
int right_ss = 0;
int compass_angle;
int orientation_tag = 0;

unsigned long pingTimer[SONAR_NUM]; // Holds the times when the next ping should happen for each sensor.
unsigned int cm[SONAR_NUM];         // Where the ping distances are stored.
uint8_t currentSensor = 0;          // Keeps track of which sensor is active.

NewPing sonar[SONAR_NUM] = {     // Sensor object array.
  NewPing(TRIGGER_HAND, ECHO_HAND, MAX_DISTANCE), // Each sensor's trigger pin, echo pin, and max distance to ping.
  //  NewPing(TRIGGER_FRONT, ECHO_FRONT, MAX_DISTANCE),
  NewPing(TRIGGER_LEFT, ECHO_LEFT, MAX_DISTANCE),
  NewPing(TRIGGER_RIGHT, ECHO_RIGHT, MAX_DISTANCE)
};

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);

  pingTimer[0] = millis() + 75;           // First ping starts at 75ms, gives time for the Arduino to chill before starting.
  for (uint8_t i = 1; i < SONAR_NUM; i++) // Set the starting time for each sensor.
    pingTimer[i] = pingTimer[i - 1] + PING_INTERVAL;
  pinMode(VIBRATOR_HAND, OUTPUT);
  pinMode(VIBRATOR_LEFT, OUTPUT);
  pinMode(VIBRATOR_RIGHT, OUTPUT);

  pinMode(BUZZER, OUTPUT);

  Wire.begin();

  // initialise compass
  compass.init();
  compass.enableDefault();

  // calibrate compass
  running_min.x = min(running_min.x, compass.m.x);
  running_min.y = min(running_min.y, compass.m.y);
  running_min.z = min(running_min.z, compass.m.z);

  running_max.x = max(running_max.x, compass.m.x);
  running_max.y = max(running_max.y, compass.m.y);
  running_max.z = max(running_max.z, compass.m.z);

  // choose axis of rotation
  compass.heading((LSM303::vector<int>) {
    0, 0, 1
  });

  // input calibration values
  compass.m_min = (LSM303::vector<int16_t>) {
    running_min.x, running_min.y, running_min.z
  };
  compass.m_max = (LSM303::vector<int16_t>) {
    running_max.x, running_max.y, running_max.z
  };

  // initialise gyrometer
  gyro.init();
  gyro.enableDefault();
  gyro.writeReg(L3G::CTRL_REG4, 0x20); // 2000 dps full scale
  gyro.writeReg(L3G::CTRL_REG1, 0x0F); // normal power mode, all axes enabled, 100 Hz

  // calibrate gyrometer
  for (int n = 0; n < sampleNum; n++) {
    gyro.read();
    dc_offset_x += (int)gyro.g.x;
    dc_offset_y += (int)gyro.g.y;
    dc_offset_z += (int)gyro.g.z;
  }

  AN_OFFSET[0] = dc_offset_x / sampleNum;
  AN_OFFSET[1] = dc_offset_y / sampleNum;
  AN_OFFSET[2] = dc_offset_z / sampleNum;
}

void readGyroAndCompass() {

  // Every 10 ms take a sample from the gyro and compass
  if (millis() - time > sampleTime)
  {
    gyro.read();
    compass.read();

    heading = compass.heading();
    compass_angle = heading;
    compass_angle += 270;

    if (compass_angle >= 360) {
      compass_angle -= 360;
    }

    AN[0] = gyro.g.x;
    AN[1] = gyro.g.y;
    AN[2] = gyro.g.z;

    gyro_z = SENSOR_SIGN[0] * (AN[0] - AN_OFFSET[0]);
    gyro_y = SENSOR_SIGN[1] * (AN[1] - AN_OFFSET[1]);
    gyro_x = SENSOR_SIGN[2] * (AN[2] - AN_OFFSET[2]);

    time = millis(); // update the time to get the next sample
  }
}

void makeSenseOfRawValues() {

  // pedometer
  if ((gyro_z > 1000) && (gyro_y > -1000) && (gyro_y < 1000)) {
    steps = steps + 1;
    delay(200);
  }
  else if ((gyro_x > 800) && (-1000 < gyro_z) && (gyro_z < 1000)) {
    left_ss = left_ss + 1;
    delay(300);
  }
  else if ((gyro_x < -1000) && (-1000 < gyro_z) && (gyro_z < 1000)) {
    right_ss = right_ss + 1;
    delay(300);
  }
  else if ((gyro_y > 2000) && (-1000 < gyro_z) && (gyro_z < 1000)) {
    left_turn = left_turn + 1;
    delay(300);
  }
  else if ((gyro_y < -2000) && (-1000 < gyro_z) && (gyro_z < 1000)) {
    right_turn = right_turn + 1;
    delay(300);
  }

  // compass
  if (((compass_angle >= 0) && (compass_angle < 11.25)) || ((compass_angle >= 348.25) && (compass_angle < 360)))  {
    orientation_tag = 1; // north
  }
  else if ((compass_angle >= 11.25) && (compass_angle < 25.75)) {
    orientation_tag = 2; // north-north-east
  }
  else if ((compass_angle >= 25.75) && (compass_angle < 42.25)) {
    orientation_tag = 3; // north-east
  }
  else if ((compass_angle >= 42.25 ) && (compass_angle < 50.75))  {
    orientation_tag = 4; //east-north-east
  }
  else if ((compass_angle >= 50.75) && (compass_angle < 78.25)) {
    orientation_tag = 5; // east
  }
  else if ((compass_angle >= 78.25) && (compass_angle < 92.75))  {
    orientation_tag = 6; // east-south-east
  }
  else if ((compass_angle >= 92.75) && (compass_angle < 110.25)) {
    orientation_tag = 7; // south-east
  }
  else if ((compass_angle >= 110.25) && (compass_angle < 146.75)) {
    orientation_tag = 8; // south-south-east
  }
  else if ((compass_angle >= 146.75) && (compass_angle < 217.25))  {
    orientation_tag = 9; // south
  }
  else if ((compass_angle >= 217.25) && (compass_angle < 230.75)) {
    orientation_tag = 10; // south-south-west
  }
  else if ((compass_angle >= 230.75) && (compass_angle < 250.25))  {
    orientation_tag = 11; // south-west
  }
  else if ((compass_angle >= 250.25) && (compass_angle < 270.75)) {
    orientation_tag = 12; //west-south-west
  }
  else if ((compass_angle >= 270.75) && (compass_angle < 300.25)) {
    orientation_tag = 13; //west
  }
  else if ((compass_angle >= 300.25) && (compass_angle < 313.75))  {
    orientation_tag = 14; //west-north-west
  }
  else if ((compass_angle >= 313.75) && (compass_angle < 326.25)) {
    orientation_tag = 15; // north-west
  }
  else if ((compass_angle >= 326.25) && (compass_angle < 348.25))  {
    orientation_tag = 16; // north-north-west
  }
  else {
    orientation_tag = 0; // error
  }
}

void printData() {
  /*Serial.print("Steps: ");
    Serial.print(steps);
    Serial.print("\tLeft/Right Turns: ");
    Serial.print(left_turn);
    Serial.print("/");
    Serial.print(right_turn);
    //Serial.print("\tLeft/Right Side-steps: ");
    //Serial.print(left_ss);
    //Serial.print("/");
    //Serial.print(right_ss);
    Serial.print("\tA.Velocity:");
    Serial.print(AN[0] - AN_OFFSET[0]);  //(int)read_adc(0)
    Serial.print(",");
    Serial.print(AN[1] - AN_OFFSET[1]);
    Serial.print(",");
    Serial.print(AN[2] - AN_OFFSET[2]);*/
  Serial.print("\tDirection: ");

  switch (orientation_tag) {
    case 0:
      Serial.print("Error");
      break;
    case 1:
      Serial.print("N");
      break;
    case 2:
      Serial.print("NNE");
      break;
    case 3:
      Serial.print("NE");
      break;
    case 4:
      Serial.print("ENE");
      break;
    case 5:
      Serial.print("E");
      break;
    case 6:
      Serial.print("ESE");
      break;
    case 7:
      Serial.print("SE");
      break;
    case 8:
      Serial.print("SSE");
      break;
    case 9:
      Serial.print("S");
      break;
    case 10:
      Serial.print("SSW");
      break;
    case 11:
      Serial.print("SW");
      break;
    case 12:
      Serial.print("WSW");
      break;
    case 13:
      Serial.print("W");
      break;
    case 14:
      Serial.print("WNW");
      break;
    case 15:
      Serial.print("NW");
      break;
    case 16:
      Serial.print("NNW");
      break;
  }
  Serial.println();
  delay(50);
}

bool handshakeDone = false;
// PiMegaCommunication variables
int checkSum = 0;
int values[7]; // array size = 7

void loop() {
  if (handshakeDone == true) {
    for (uint8_t i = 0; i < SONAR_NUM; i++) { // Loop through all the sensors.
      if (millis() >= pingTimer[i]) {         // Is it this sensor's time to ping?
        pingTimer[i] += PING_INTERVAL * SONAR_NUM;  // Set next time this sensor will be pinged.
        if (i == 0 && currentSensor == SONAR_NUM - 1) oneSensorCycle(); // Sensor ping cycle complete, do something with the results.
        sonar[currentSensor].timer_stop();          // Make sure previous timer is canceled before starting a new ping (insurance).
        currentSensor = i;                          // Sensor being accessed.
        cm[currentSensor] = 0;                      // Make distance zero in case there's no ping echo for this sensor.
        sonar[currentSensor].ping_timer(echoCheck); // Do the ping (processing continues, interrupt will call echoCheck to look for echo).
      }
    }
    // Other code that *DOESN'T* analyze ping results can go here.
    readGyroAndCompass();
    makeSenseOfRawValues();
  }

  //Poll command sent from pi
  if (Serial1.available()) {
    int inByte = Serial1.read();

    if (inByte == 'H') { // HELLO
      Serial.println('H');
      Serial1.print('A');
    }

    if (inByte == 'A') { // Acknowledge
      Serial.println('A');
      Serial.println("Pi is ready");
      handshakeDone = true;
    }

    if (inByte == 'P') {
      // Serial.println();
      startAtomic();
      values[0] = cm[0]; // Ultrasonic sensor cm[0]-cm[3]
      values[1] = 123;
      values[2] = cm[1];
      values[3] = cm[2];
      values[4] = steps;
      values[5] = orientation_tag;
      endAtomic();

      // DEBUGGING
      Serial.println(cm[0]);
      Serial.println(123);
      Serial.println(cm[1]);
      Serial.println(cm[2]);

      for (int i = 0; i < 6; i++) {
        checkSum += values[i];
        Serial1.println(values[i]);
      }

      values[6] = checkSum;
      Serial1.println(values[6]);
      Serial.print("CheckSum:");
      Serial.println(checkSum);
      checkSum = 0;
    }
  }
}

void echoCheck() { // If ping received, set the sensor distance to array.
  if (sonar[currentSensor].check_timer())
    cm[currentSensor] = sonar[currentSensor].ping_result / US_ROUNDTRIP_CM;
}

int remapHand(int value) {
  // output = output_start + ((output_end - output_start) / (input_end - input_start)) * (input - input_start)
  int remap = (value - 0) * (255 - 0) / (90 - 0) + 0;
  return 255 - remap;
}

int remapSide(int value) {
  int remap = (value - 0) * (255 - 0) / (50 - 0) + 0;
  return 255 - remap;
}

void oneSensorCycle() { // Sensor ping cycle complete, do something with the results.
  // The following code would be replaced with your code that does something with the ping results.
  //  for (uint8_t i = 0; i < SONAR_NUM; i++) {
  //    Serial.print(i + 1);
  //    Serial.print("=");
  //    Serial.print(cm[i]);
  //    Serial.print("\t");
  //  }
  //  Serial.println();

  if (cm[0] < 91 and cm[0] > 6) {
    int hand = remapHand(cm[0]);
    analogWrite(VIBRATOR_HAND, hand);
    if (cm[0] < 26 and cm[0] != 0) {
      digitalWrite(BUZZER, HIGH);
      delay(5);
      digitalWrite(BUZZER, LOW);
    }
  } else {
    digitalWrite(VIBRATOR_HAND, LOW);
  }

  if (cm[1] < 46 and cm[1] > 6) {
    int remapLeft = remapSide(cm[1]);
    analogWrite(VIBRATOR_LEFT, remapLeft);
  } else {
    digitalWrite(VIBRATOR_LEFT, LOW);
  }

  if (cm[2] < 46 and cm[2] > 6) {
    int remapRight = remapSide(cm[2]);
    analogWrite(VIBRATOR_RIGHT, remapRight);
  } else {
    digitalWrite(VIBRATOR_RIGHT, LOW);
  }
}

void startAtomic() {
  cli();
}

void endAtomic() {
  sei();
}

