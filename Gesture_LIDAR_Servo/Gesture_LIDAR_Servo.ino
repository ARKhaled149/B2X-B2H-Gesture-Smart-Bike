#include <SoftwareSerial.h>
#include <Servo.h>
#include <LiquidCrystal.h>
SoftwareSerial Serial1(10,11);
Servo Myservo;
const int SERVO_PIN = 9;
int x;
boolean shit;
void setup() {
  Serial.begin(9600); 
  Myservo.attach(SERVO_PIN);
  shit = false;
}
void loop() {   
  if (Serial.available()) {
     x  = Serial.readStringUntil('\n').toInt();
     Serial.println(x);
   }
  if (x == 5){
    
      Myservo.write(80);
      delay(10);
      
   }
   else{
      Myservo.write(180);
      delay(10);
   }
  delay(10);
}
