#ifndef Segmentdriver_h
#define Segmentdriver_h

#include "Arduino.h"
#include "Ioexpander.h"   //gebruikt IOExpander
#define I2C_SEG_ADR 0x3A   //adress SEG
class Segmentdriver{
    private:
        Ioexpander *ioe;
    public:
        Segmentdriver(uint8_t address);
        void init();   //initialisatie segment
        void write_value(uint8_t val);   //getal op segment schrijven
};

#endif 