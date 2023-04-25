#ifndef Serial_driver_h
#define Serial_driver_h

void serialUSB_begin();    //initialisatie van USB serial

bool serial_signal();   //detecteerd inkomend signaal 
bool serial_signal_vib();  //origineel om  vibrator te detecterne nu via   algemene fct serial_signal en switch case in main
bool serial_signal_buz();  //origineel om  buzzer te detecterne nu via   algemene fct serial_signal en switch case in main


#endif