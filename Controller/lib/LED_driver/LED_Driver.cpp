#include "LED_driver.h"

LED_driver::LED_driver(uint8_t address){
    this->ioe=new Ioexpander(address);
}

void LED_driver::init(){
    this->ioe->init();
    this->ioe->set_conf_reg(0x00);
}

void LED_driver::write_value(uint8_t val){

    switch(val){
        case 0: ioe->set_output_reg(0x00);break; // geen items gecollect
        case 1: ioe->set_output_reg(0x80);break; // 1 item (zonder gsm)
        case 2: ioe->set_output_reg(0xC5);break; // 2 item (zonder gsm)
        case 3: ioe->set_output_reg(0xE5);break; // 3 items (zonder gsm)
        case 4: ioe->set_output_reg(0xF5); break; // 4 items (zonder gsm)
        case 5: 
                    ioe->set_output_reg(0x08);    // 1 item (gsm)
                    delay(1000);
                    ioe->set_output_reg(0x00);
                    delay(1000);
                    break;
      case 6: 
                ioe->set_output_reg(0x88); // 2 items (gsm)
                break;
      case 7: 
                ioe->set_output_reg(0xC8); // 3 items (gsm)
                break;
      case 8: ioe->set_output_reg(0xE8); // 4 items (gsm)
                break;
      case 9: ioe->set_output_reg(0xFF); // 5 items (gsm)
                break;
    default: break;
    }
}
