/********************************************************
 * PID Adaptive Tuning Example
 * One of the benefits of the PID library is that you can
 * change the tuning parameters at any time.  this can be
 * helpful if we want the controller to be agressive at some
 * times, and conservative at others.   in the example below
 * we set the controller to use Conservative Tuning Parameters
 * when we're near setpoint and more agressive Tuning
 * Parameters when we're farther away.
 ********************************************************/

#include <PID_v1.h>
#include <Filters.h>
// ONLY_CHANGE THE MOTOR PINS PIN_OUTPUT_1 and PIN_OUTPUT_2
#define ENABLE 4
#define PIN_INPUT A7
#define PIN_OUTPUT_1 5
#define PIN_OUTPUT_2 6

//Define Variables we'll be connecting to
double Setpoint, Input, Output;
int inputValue = -1;  // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete
//Define the aggressive and conservative Tuning Parameters
double aggKp=4, aggKi=0.2, aggKd=1;
double consKp=1, consKi=0.05, consKd=0.25;
double cmd;
//double l1 = 65; 
//double r1 = 115; 
//double l2 = 225; 
//double r2 = 775; 


double l1 = 65; 
double r1 = 125; 
double l2 = 230; 
double r2 = 850; 

//double l1 = 50; 
//double r1 = 130; 
//double l2 = 230; 
//double r2 = 850; 


//Specify the liString.replace("⸮",nks and initial tuning parameters
PID myPID(&Input, &Output, &Setpoint, consKp, consKi, consKd, DIRECT);
//FilterOnePole lowpassFilter( LOWPASS, 5 );
FilterOnePole lowpassFilter( LOWPASS, 5 );
void setup()
{
//  pinMode(5,OUTPUT);
//  pinMode(10,OUTPUT);

  pinMode(PIN_OUTPUT_1,OUTPUT);
  pinMode(PIN_OUTPUT_2,OUTPUT);
  pinMode(ENABLE,OUTPUT);
  Serial.begin(9600);
  digitalWrite(ENABLE,HIGH);
  digitalWrite(PIN_OUTPUT_1,HIGH);
  digitalWrite(PIN_OUTPUT_2,HIGH);
  //initialize the variables we're linked to
  Input = analogRead(PIN_INPUT);
  Setpoint = 512;

  //turn the PID on
  myPID.SetMode(AUTOMATIC);
  cmd=90.0;
}

void loop()
{
//  inputValue = 45;
//  inputValue = map(inputValue, l1,r1, r1,l1);
    Input = analogRead(PIN_INPUT);
    Serial.println(Input); // to see if the potentiometer is working
    if(inputValue<l1){inputValue =l1;}
    if(inputValue>r1){inputValue =r1;}
    if(inputValue>=l1 && inputValue<=r1){
      cmd = inputValue;
      Input = analogRead(PIN_INPUT);
      Serial.println(Input); // to see if the potentiometer is working
      Input = int(lowpassFilter.input(Input)); 
//      Setpoint = map(cmd, l1,r1, r1,l1);
      Setpoint = map(cmd, l1,r1, l2,r2);
        
  //    Setpoint = cmd;
      double gap = abs(Setpoint-Input); //distance away from setpoint
//      Serial.println(gap);
//      Serial.println();
      if(gap < 750)
      {  //we're close to setpoint, use conservative tuning parameters
        myPID.SetTunings(consKp, consKi, consKd);
        myPID.Compute();
        analogWrite(PIN_OUTPUT_1 , Output * (Output>0));
        analogWrite(PIN_OUTPUT_2 , -Output * (Output<0));
      }
      else
      {
         //we're far from setpoint, use aggressive tuning parameters
         myPID.SetTunings(aggKp, aggKi, aggKd);
      }
    

          
      stringComplete = false;
      delay(50);
    }
    else{
         analogWrite(PIN_OUTPUT_1 , 0);
         analogWrite(PIN_OUTPUT_2 , 0);
    }
    
//  char steer = Serial.read();
//  int steer = Serial.parseInt();
//  Serial.println(steer);
//  delay(100);
//  if(steer == '0'){
//    cmd = 275;
//    
//    }
//  else if(steer == '1'){
//    cmd = 325;
//    }
//  else if(steer == '2'){
//    cmd = 425;
//  }
//  else if(steer == '3'){
//    cmd = 512;
//  }
//  else if(steer == '4'){
//    cmd = 625;
//  }
//  else if(steer == '5'){
//    cmd = 725;
//  }
//  else if(steer == '6'){
//    cmd = 775;
//  }
//  else{
//    Serial.println("kkkkkk1");
//    }
//  Serial.setTimeout(10);
//  cmd = Serial.parseFloat();
  
}

 
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    //for(int i = 0;i <30;i++){
    int command = Serial.read();
    if (command == 0xFF) {
      Serial.write('S');
    } else {
      inputValue = command;
    }
    
    //Serial.println(command);
    
//    inputString += inChar;
//    Serial.println(inChar);
    //inputString.replace("⸮","");
   /// }
 ///   inputString.replace("[2J[1;1","m ");
   // stringComplete = true;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
  
  //if (inputString.endsWith("\n")) {
      //stringComplete = true;
   // }
  }
//  inputValue=-1;
  

}
