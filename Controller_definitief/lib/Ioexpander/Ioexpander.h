#ifndef Ioexpander_h
#define Ioexpander_h

#include "Arduino.h"
#include "Wire.h"


class Ioexpander{
    public:
        Ioexpander(uint8_t address);
        void init();
        void set_conf_reg(uint8_t reg_byte);
        void set_output_reg(uint8_t reg_byte);
    private:
        int _address;
};

#endif