#ifndef Vibrator_h
#define vibrator_driver_h
#include <Arduino.h>
const int vib=12;   //vibrator pin 1
const int vib2=5;   //vibrator pin 2
void vibrate_begin();
void vibrate(int strength,long duration);


#endif