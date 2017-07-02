#include <AccelStepper.h>
#define HALFSTEP 8

// Motor pin definitions
#define motorPin1  3     // IN1 on the ULN2003 driver 1
#define motorPin2  4     // IN2 on the ULN2003 driver 1
#define motorPin3  5     // IN3 on the ULN2003 driver 1
#define motorPin4  6     // IN4 on the ULN2003 driver 1
#define sensor_start A0
#define sensor_end A1

enum BridgeState {WAITING_MARBLE, COUNTDOWN_PREP, COUNTDOWN_60, RELEASE_MARBLE, DETECT_FINISH, SUCCESS, FAIL, CODE};

BridgeState STATE;

AccelStepper stepper1(HALFSTEP, motorPin1, motorPin3, motorPin2, motorPin4);

int counter = 0;

unsigned long some_time;


void setup() {
  Serial.begin(9600);
  stepper1.setMaxSpeed(50000.0);
  stepper1.setAcceleration(5000.0);
  stepper1.setSpeed(20000);
  pinMode(sensor_start, INPUT);
  pinMode(sensor_end, INPUT);
  STATE =  WAITING_MARBLE;
  Serial.println("Loading...");
  start_motor();


}

bool detect_marble_start() {
  int sensorVal_Begin = analogRead(sensor_start);
  if (sensorVal_Begin > 800) {
    return true;
  }
  return false;
}

bool detect_marble_end() {
  int sensorVal_End = analogRead(sensor_end);
  while (sensorVal_End > 800) {
    return true;
  }
  return false;
}

void start_motor() {
  stepper1.moveTo(-2000);
  while (stepper1.distanceToGo() < 0)
  {
    stepper1.run();
  }
  delay(3000);
  stepper1.moveTo(0);
  while (stepper1.distanceToGo() > 0)
  {
    stepper1.run();
  }
}


void loop() {

  switch (STATE)
  {
    case WAITING_MARBLE:
      Serial.println("W waiting marble");

      while ( !detect_marble_start() ) {
        delay(10);
      }
      STATE = COUNTDOWN_PREP;
      break;

    case COUNTDOWN_PREP:
      Serial.println("C Ready");
      delay(3000);
      Serial.println("C Start");
      STATE = COUNTDOWN_60;
      counter = 60;
      delay(1000);

      break;


    case COUNTDOWN_60:
      //Serial.println("C 1");

      while (counter > 1) {
        counter--;
        Serial.print("C ");
        Serial.println(counter);
        delay(1000);

      }
      STATE = RELEASE_MARBLE;

      break;

    case RELEASE_MARBLE:
      Serial.println("C Finish");

      start_motor();
      STATE = DETECT_FINISH;

      //Serial.println ("Marble Released");
      some_time = millis();
      break;

    case DETECT_FINISH:
      STATE = FAIL;
      while (millis() - some_time < 20000) {  //wait for 20s to allow marble to
        if (detect_marble_end()) {
          STATE = SUCCESS;
          Serial.println("P SUCCESS");
          break;
        }
      }
      some_time = millis();
      counter = 3;
      break;

    case SUCCESS:
      delay(5000);
      Serial.println("P CODE");
      delay(10000);

      //Serial.println(""); //hints go in here
      STATE = WAITING_MARBLE;
      break;

    case FAIL:
      Serial.println("P TRY AGAIN");
      delay(10000);
      STATE = WAITING_MARBLE;
      break;
  }
}

