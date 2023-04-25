#include "Segmentdriver.h"

Segmentdriver::Segmentdriver(uint8_t address){ 
    this->ioe=new Ioexpander(address);
}

void Segmentdriver::init(){
    this->ioe->init();
    this->ioe->set_conf_reg(0x00);
}

void Segmentdriver::write_value(uint8_t val){

    switch(val){
        case 0: ioe->set_output_reg(0x36);break;
        case 1: ioe->set_output_reg(0x37);break;
        case 2: ioe->set_output_reg(0x77);break;
        case 3: ioe->set_output_reg(0x7F);break;

    default: break;
    }
}