#include <Arduino.h>
#include "Buzzerdriver.h"
//buzzer is de pin 
//tone(buzzer,100);
  //delay(1000);
  //noTone(1000);
  //delay(1000);

void buzzer_begin(){
    pinMode(buzzer,OUTPUT);
}






void buzzer_push(long duration,int frequency){
    //tone(buzzer,100,duration);
    tone(buzzer,frequency,duration);
    
}