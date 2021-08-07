#include <EEPROM.h>
#include <SoftwareSerial.h>
#include <Servo.h>
#include <LiquidCrystal.h>
//#include <PID_v1.h>
///#include <Filters.h>
// ONLY_CHANGE THE MOTOR PINS PIN_OUTPUT_1 and PIN_OUTPUT_2
//#define ENABLE 4
//#define PIN_INPUT A1
//#define PIN_OUTPUT_1 5
//#define PIN_OUTPUT_2 6
SoftwareSerial Serial1(10,11);
Servo Myservo;
const int SERVO_PIN = 9;
int x;
const int in1 = 5;
const int in2 = 6;
const int pot = A1;
double kp = 4;
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
double Setpoint, Input, Output;
int inputValue = -1;
boolean stringComplete = false;
double cmd;
double l1 = -30; 
double r1 = 30; 
double l2 = 865; 
double r2 = 885; 
void setup(){
  setPoint = 0;                         
  Serial.begin(9600);
  Myservo.attach(SERVO_PIN);
  Myservo.write(180);
  delay(10);  
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
//  Serial.println(setPoint);
  float i1 = analogRead(pot);
  input = map(i1,184,200,-30, 30);
  Serial.println(i1);  
  //Serial.println(input);
  output = computePID(setPoint,input);
  // handle direction of rotation
  if(output > 0){
      analogWrite(in2, 0);
      analogWrite(in1, 0);
      delay(10);
    }
    else{
      analogWrite(in2, 0);
      analogWrite(in1, 0);
      delay(10);
    }
}

double computePID(double desired, double inp){    
        currentTime = millis();                                     //get current time
        elapsedTime = (double)(currentTime - previousTime);         //compute time elapsed from previous computation
        error = desired - inp;                                      // determine error
        cumError += error * elapsedTime;                            // compute integral
        double out = kp*error + ki*cumError;                        //PID output              
        lastError = error;                                          //remember current error
        previousTime = currentTime;                                 //remember current time
        if(out > 255){
          out = 255;
        }
        if(out < -255){
          out = -255;
        }
        return out;                  
}
