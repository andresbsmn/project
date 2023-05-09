//driver voor buttons+work in progress
#ifndef Button_Driver_h
#define Button_Driver_h
#include <Arduino.h>
#include "HID-Project.h"

const int pinButtonForward = 15;  
const int pinButtonBackward = 17;
const int pinButtonLeft = 14;
const int pinButtonRight = 16;  

const int pinLEDA = 6;  
const int pinLEDB = 39;
const int pinLEDC = 8;
const int pinLEDD = 9; 



void button_ini();
void move(int pinButton, char character);
#endif