#ifndef Buzzerdriver_h
#define Buzzerdriver_h
const int buzzer=2; //pin van buzzer
void buzzer_begin();   // initialiseert buzzer
void buzzer_push(long duration,int frequency);

#endif