#include "Ioexpander.h"

Ioexpander::Ioexpander(uint8_t address){
    this->_address=address;
}

void Ioexpander::init(){
    Wire.begin();
}

void Ioexpander::set_conf_reg(uint8_t reg_byte){
    Wire.beginTransmission(this->_address);
    Wire.write(0x03);
    Wire.write(reg_byte);
    Wire.endTransmission();
}

void Ioexpander::set_output_reg(uint8_t reg_byte){
    Wire.beginTransmission(this->_address);
    Wire.write(0x01);
    Wire.write(reg_byte);
    Wire.endTransmission();
}

