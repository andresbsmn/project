#ifndef LED_driver_h
#define LED_driver_h

#include "Arduino.h"
#include "Ioexpander.h"
#define I2C_ADR 0x3B 
class LED_driver{
    private:
        Ioexpander *ioe;
    public:
        LED_driver(uint8_t address);
        void init();
        void write_value(uint8_t val);
};

#endif 