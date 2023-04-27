#include "Serial_driver.h"
#include <Arduino.h>



void serialUSB_begin(){
    SerialUSB.begin(9600);
}

bool serial_signal(){
    if (SerialUSB.available() > 0){
        return true;
    }else{
        return false;
    }
}

    
        
    
/* bool serial_signal(){
    if (SerialUSB.available() > 0) {               // controleer of er gegevens beschikbaar zijn op de seriële poort
        char receivedChar = SerialUSB.read();           // lees het ontvangen teken
        if (receivedChar == '1') {                      // controleer of het teken "1" is
            return true;
        }else{
            return false;
        }
    }else{
        return false;
    }
}

*/

/*
bool serial_signal_vib(){
    if (SerialUSB.available() > 0) {               //detecteerd char v dan ist vibrator.        
        if (SerialUSB.read() == 'v') {                      
            return true;
        //}else{
        //    return false;
        }
    //}else{
    //    return false;
    }
    return false;
}


bool serial_signal_buz(){                           //detecteer char b dan ist buzzer.
     if (SerialUSB.available() > 0) {                        
        if (SerialUSB.read() == 'b') {                     
            return true;
        //}else{
        //    return false;
        }
    //}else{
    //    return false;
    }
    return false;
}

*/