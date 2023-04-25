#include "CapacitiveTouch_driver.h"


void capacitive_ini(){
    pinMode(CapacitivePin, INPUT_PULLUP);
    pinMode(pinLED,OUTPUT);
    
}

void save(){
  
  
  if(digitalRead(CapacitivePin) == HIGH){
    Keyboard.press('p');  //dit p en release moet terug uit commentaar uiteindelijk
    digitalWrite(pinLED,HIGH);
    
  }else{
    digitalWrite(pinLED,LOW);
    Keyboard.release('p');
  }
  
}