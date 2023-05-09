#include "Button_Driver.h"

void button_ini(){
    pinMode(pinButtonForward, INPUT_PULLUP);
    pinMode(pinButtonBackward, INPUT_PULLUP);
    pinMode(pinButtonLeft, INPUT_PULLUP);
    pinMode(pinButtonRight, INPUT_PULLUP);
    
    pinMode(pinLEDA, OUTPUT);
    pinMode(pinLEDB,  OUTPUT);
    pinMode(pinLEDC,  OUTPUT);
    pinMode(pinLEDD,  OUTPUT);
    digitalWrite(pinLEDA,HIGH);
    digitalWrite(pinLEDB,HIGH);
    digitalWrite(pinLEDC,HIGH);
    digitalWrite(pinLEDD,HIGH);
    
}

void move(int pinButton, char character){


  
  if (digitalRead(pinButton) == LOW){
    //Keyboard.write('a');
    Keyboard.press(character);
    //delay(100);  //kan weg denk ik

  }
  else{
    Keyboard.release(character);
  }
}