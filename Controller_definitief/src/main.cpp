#define HID_CUSTOM_LAYOUT  //hid layout 
#define LAYOUT_FRENCH_BELGIAN //hid layout miss later verplaatsen
#include <Arduino.h>     //lol standaard
#include "HID-Project.h"   //regelt communicatie naar controller
#include "Buzzerdriver.h"    //buzzer
#include "Serial_driver.h"  //regel ontvangst controller
#include "Vibrator.h"   //vibrator
#include "HID.cpp" //HID besturing 
#include "Segmentdriver.h" //segment aansturing
#include "LED_Driver.h"   //LED aansturing 
#include "Button_Driver.h"
#include "CapacitiveTouch_driver.h"
#include "Lumen_Driver.h"
#include "Gyro_Driver.h"
#include "Buig_Driver.h"


#define I2C_ADR 0x3B 
Segmentdriver segment1(0x3A); //segment objectl
LED_driver LED(0x3B); //led object
bool gamegestart = false;
void setup() {
  // put your setup code here, to run once:
  LED.init(); //LED operaties starten
  segment1.init();  //segment operaties initialiseren
  vibrate_begin(); //vibrator functies starten
  buzzer_begin(); //buzzer functies starten
  serialUSB_begin(); //vanaf nu leest serialusb alles in
  button_ini();
  capacitive_ini();
  gyro_ini();
  light_ini();
  Keyboard.begin();
  // code andres pinMode(pinButton,INPUT_PULLUP);
  //code andres Keyboard.begin();
}

void loop() {

  if(serial_signal()){
    switch(SerialUSB.read()){
    case '0': segment1.write_value(0); break;  //1  hartje
    case '1': segment1.write_value(1); break; // 2 hartjes
    case '2': segment1.write_value(2); break; //3 hartjes
    case '3': segment1.write_value(3); break; //0 hartjes
    case '4':LED.write_value(0); break;       //geen items gecollectl
    case '5':LED.write_value(1); break;       //1 item (zonder gsm)
    case '6':LED.write_value(2); break;       //2 items (zonder gsm)
    case '7':LED.write_value(3); break;       //3 items (zonder gsm)
    case '8':LED.write_value(4); break;       //4 items (zonder gsm)
    case '9':LED.write_value(5); break;       //1 item (met gsm)
    case 'a':LED.write_value(6); break;      //2 items (met gsm)
    case 'z':LED.write_value(7); break;      //3 items (met gsm)
    case 'e':LED.write_value(8); break;      //4 items (met gsm)
    case 'r':LED.write_value(9); break;      //5 items (met gsm)
    case 'b':buzzer_push(250,800);  break;              //buzzer buzz 250 ms 
    case 'v':vibrate(255,300); break; 
    case 's':gamegestart = !gamegestart; delay(100); break;
    default:  break;
    } 
  }


  
  move(pinButtonForward, 'w');  //forward  15
  move(pinButtonBackward, 's'); //
  move(pinButtonLeft, 'a'); //
  move(pinButtonRight, 'd');  //


  if(gamegestart){
    save();
    light();
    gyro();
    buigsensor();
  }
  
}
