#include <MPU6050_tockn.h>
#include <EEPROM.h>
#include <SoftwareSerial.h>
#include <Servo.h>
#include <LiquidCrystal.h>
//#include <PID_v1.h>
//#include <Filters.h>
// ONLY_CHANGE THE MOTOR PINS PIN_OUTPUT_1 and PIN_OUTPUT_2
//#define ENABLE 4
//#define PIN_INPUT A1
//#define PIN_OUTPUT_1 5
//#define PIN_OUTPUT_2 6
SoftwareSerial Serial1(10,11);//  Serial.println(setPoint);

Servo Myservo;
const int SERVO_PIN = 9;
int x;
const int in1 = 10;
const int in2 = 11; 
const int pot = A1;
double kp = 10;
double ki = 0.00;
unsigned long currentTime, previousTime;
double elapsedTime;
double error;
double lastError;
double input, output, setPoint;
double cumError,desired;
int serv;
int ang;
int gesture;
int servo;
String x2;
int koko;
MPU6050 mpu6050(Wire);
//Define Variables we'll be connecting to
double Setpoint, Input, Output;
int inputValue = -1;
// a string to hold incoming data
boolean stringComplete = false;
// whether the string is complete
//Define the aggressive and conservative Tuning Parameters
//double aggKp=4, aggKi=0.2, aggKd=1;
//double consKp=1, consKi=0.05, consKd=0.25;
double cmd;
double l1 = -30; 
double r1 = 30; 
double l2 = 865; 
double r2 = 885; 
//PID myPID(&Input, &Output, &Setpoint, consKp, consKi, consKd, DIRECT);
//
void setup(){
  setPoint = 0;                          //set point at zero degrees
  Serial.begin(9600);
  Myservo.attach(SERVO_PIN);
  Myservo.write(180);
  delay(10); 
   Wire.begin();
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true); 
}    

void loop(){  
    if (Serial.available()) {
      x2  = Serial.readStringUntil('\n');
      Serial.println(x2);
      x = x2.substring(0,1).toInt();
      koko = (x2.substring(2,x2.length())).toInt();
      if (x == 5){
        Myservo.write(30);
        delay(10);
       }
       else{
          Myservo.write(180);
          delay(10);
        }
      }
  //Serial.print("desired: ");
  setPoint = koko;
    mpu6050.update();

  input = round(mpu6050.getAngleZ());
  output = computePID(setPoint,input);
      Serial.println("-------------------");

    Serial.println(input);
    Serial.println(output);
    Serial.println("-------------------");

//  Serial.println(output);
  // handle direction of rotation
  if(output > 0){
      analogWrite(in2, output);
      analogWrite(in1, 0);
      delay(10);
    }
    else{
      analogWrite(in2, 0);
      analogWrite(in1, output*-1);
      delay(10);
    }
   // Serial.print("control effort: ");
   // Serial.println(output);
}

double computePID(double desired, double inp){    
        currentTime = millis();                //get current time
        elapsedTime = (double)(currentTime - previousTime);        //compute time elapsed from previous computation
        error = desired - inp;                                // determine error
        cumError += error * elapsedTime;                // compute integral
        double out = kp*error + ki*cumError;                //PID output              
        lastError = error;                                //remember current error
        previousTime = currentTime;                        //remember current time
        if(out > 255){
          out = 255;
        }
        if(out < -255){
          out = -255;
        }
        return out;                  
}
