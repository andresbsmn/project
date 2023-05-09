#include "Vibrator.h"
void vibrate_begin(){
    pinMode(vib,OUTPUT);
    pinMode(vib2,OUTPUT);
}


/*
void vibrate(long duration){
        digitalWrite(vib,HIGH);   
        digitalWrite(vib2,HIGH);
        delay(duration);
        digitalWrite(vib,LOW);l
        digitalWrite(vib2,LOW); 
}
*/

void vibrate(int strength, long duration) {
  // Calculate the PWM duty cycle based on the desired strength
  int pwmValue = map(strength, 0, 100, 0, 255);

  // Turn on the PWM signals to the vibrators
  analogWrite(vib, pwmValue);
  analogWrite(vib2, pwmValue);

  // Wait for the specified duration
  delay(duration);

  // Turn off the PWM signals to the vibrators
  analogWrite(vib, 0);
  analogWrite(vib2, 0);
}


