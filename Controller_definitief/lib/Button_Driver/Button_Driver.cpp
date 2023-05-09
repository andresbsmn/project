#include "Button_Driver.h"

void button_ini(){
    pinMode(pinButtonForward, INPUT_PULLUP);
    pinMode(pinButtonBackward, INPUT_PULLUP);
    pinMode(pinButtonLeft, INPUT_PULLUP);
    pinMode(pinButtonRight, INPUT_PULLUP);
    
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