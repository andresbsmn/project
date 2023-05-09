//licht sensor driver bolleke 5


#ifndef Lumen_Driver_h
#define Lumen_Driver_h
#include <Arduino.h>
#include <Adafruit_VEML7700.h>

const int pinLed=13;

void light_ini();
void shoot();
void light();

#endif