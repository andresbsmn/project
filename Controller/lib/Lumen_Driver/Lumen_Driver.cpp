#include "Lumen_Driver.h"
#include "HID-Project.h"
Adafruit_VEML7700 veml = Adafruit_VEML7700();

void light_ini(){
  if(!veml.begin()){
      while(1);
    }
    veml.setLowThreshold(10000);
    veml.setHighThreshold(20000);    
    veml.interruptEnable(true);
}

void shoot(){
  Keyboard.press('t');
  delay(100);
  Keyboard.release('t'); //xxxx
}

void light(){
  //SerialUSB.println(veml.readLux()); 
  
  if(veml.readLux()>50.0){
      digitalWrite(pinLed, HIGH);
      shoot();
      delay(1000);
  }
  else{
    digitalWrite(pinLed, LOW);
  }
  
uint16_t irq = veml.interruptStatus();
  if(irq & VEML7700_INTERRUPT_LOW){
    SerialUSB.println("Low threshold");
  }
  if(irq & VEML7700_INTERRUPT_HIGH){
    SerialUSB.println("High threshold");
  }
  
}
  //delay(500);