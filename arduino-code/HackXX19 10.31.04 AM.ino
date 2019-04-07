//This demo is used for testing the Motor module.
#include "UCMotor.h"
#include <Servo.h>

#define SERVO_PIN 10

UC_DCMotor leftMotor1(3, MOTOR34_64KHZ);
UC_DCMotor rightMotor1(4, MOTOR34_64KHZ);
UC_DCMotor leftMotor2(1, MOTOR34_64KHZ);
UC_DCMotor rightMotor2(2, MOTOR34_64KHZ);

  //SETUP FOR ULTRASONIC SENSOR
  #define TRIG_PIN A2 //USS pin
  #define ECHO_PIN A3 //USS pin

Servo servo;
char serialread;
int angle = 90;

//SETUP FOR ULTRASONIC SENSOR
int startCount; //where we begin counting from for timing USS distance
long duration; //duration- the time it takes for audio wave to return
int distance; //distance - calculated distance in cm

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  servo.attach(SERVO_PIN);
  servo.write(angle);
  delay(500);
  servo.detach();
  delay(100);


  //SETUP FOR ULTRASONIC SENSOR
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {

  if (Serial.available() > 0) {
                // read the incoming byte:
                serialread = Serial.read();
                unsigned char c = serialread & 0xff;
                
                if(c == 0x77){ //'w'
                  if(readDistance() < 30){
                    moveServoLeft();
                    moveServoRight();
                    moveServoRight();
                    moveServoLeft();
                    }
                  else {moveForward();}
                }
                else if(c == 0x73){ //'s'
                  moveBackward();
                }
                else if(c == 0x61){ //'a'
                  moveLeft();
                }
                else if(c == 0x64){ //'d'
                  moveRight();
                }
                else if(c == 0x71){ //'q'
                  moveServoLeft();
                }
                else if(c == 0x65){ //'e'
                  moveServoRight();
                }
                else if(c == 0x72){ //'r'
                  readDistance();
                }
        }
}
void moveForward() {
        leftMotor1.run(0x01); rightMotor1.run(0x01);
        leftMotor2.run(0x01); rightMotor2.run(0x01);
        leftMotor1.setSpeed(200); rightMotor1.setSpeed(200);
        leftMotor2.setSpeed(200); rightMotor2.setSpeed(200);
        delay(400);
        leftMotor1.setSpeed(00); rightMotor1.setSpeed(00);
        leftMotor2.setSpeed(00); rightMotor2.setSpeed(00);
        delay(100);
}


void moveBackward(){
        leftMotor1.run(0x02); rightMotor1.run(0x02);
        leftMotor2.run(0x02); rightMotor2.run(0x02);
        leftMotor1.setSpeed(200); rightMotor1.setSpeed(200);
        leftMotor2.setSpeed(200); rightMotor2.setSpeed(200);
        delay(400);
        leftMotor1.setSpeed(00); rightMotor1.setSpeed(00);
        leftMotor2.setSpeed(00); rightMotor2.setSpeed(00);
        
}

void moveLeft(){
        leftMotor1.run(0x03); rightMotor1.run(0x03);
        leftMotor2.run(0x03); rightMotor2.run(0x03);
        leftMotor1.setSpeed(200); rightMotor1.setSpeed(200);
        leftMotor2.setSpeed(200); rightMotor2.setSpeed(200);
        delay(200); 
        leftMotor1.setSpeed(00); rightMotor1.setSpeed(00);
        leftMotor2.setSpeed(00); rightMotor2.setSpeed(00);
        delay(100);
}

void moveRight(){  
        leftMotor1.run(0x04); rightMotor1.run(0x04);
        leftMotor2.run(0x04); rightMotor2.run(0x04);
        leftMotor1.setSpeed(200); rightMotor1.setSpeed(200);
        leftMotor2.setSpeed(200); rightMotor2.setSpeed(200);
        delay(200);      
        leftMotor1.setSpeed(00); rightMotor1.setSpeed(00);
        leftMotor2.setSpeed(00); rightMotor2.setSpeed(00);
        delay(100);
}

void moveServoLeft(){
  angle += 30;
  servo.attach(SERVO_PIN);
  servo.write(angle);
  delay(200);
  servo.detach();
}
void moveServoRight(){
  angle -= 30;
  servo.attach(SERVO_PIN);
  servo.write(angle);
  delay(200);
  servo.detach();
}

//METHODS FOR ULTRASONIC SENSOR
int readDistance(){
  //clears trigPin
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  //sets the trigPin on HIGH for 10 micro seconds
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  //reads echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(ECHO_PIN, HIGH);
  //calculate distance
  distance = duration*0.034/2;
  Serial.println(distance);
  return distance;
  }


  
  
