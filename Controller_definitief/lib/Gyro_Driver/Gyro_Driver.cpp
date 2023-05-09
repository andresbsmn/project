
#include "Gyro_Driver.h"
#include "HID-Project.h"
Adafruit_MPU6050 mpu = Adafruit_MPU6050();
void gyro_ini(){
    mpu.setMotionInterrupt(true);
    if(!mpu.begin()){
      while(1);
    }
    //https://github.com/adafruit/Adafruit_MPU6050/blob/master/examples/motion_detection/motion_detection.ino
    mpu.setHighPassFilter(MPU6050_HIGHPASS_0_63_HZ);
    mpu.setMotionDetectionThreshold(2);
    mpu.setMotionDetectionDuration(20);
    mpu.setInterruptPinLatch(true);	// Keep it latched.  Will turn off when reinitialized.pppppppppppppppppppppppppppp
    mpu.setInterruptPinPolarity(true);
    mpu.setMotionInterrupt(true);
}



void Schrijfrichting(char richting){
      Keyboard.press(richting);
      delay(75);
      Keyboard.release(richting);

}

void gyro(){//pos y-as is rechts g.gyro.y
    // if(mpu.getMotionInterruptStatus()) {}
        sensors_event_t a, g, temp;
        mpu.getEvent(&a, &g, &temp);
        int hoeveel = round((a.gyro.y));
        //if(hoeveel<0){hoeveel = -hoeveel;}//zodat het pos blijft
        //char hoeveel_char = intToChar(hoeveel);
        if(a.gyro.y>dode_hoek){
            if(hoeveel<2){
                Schrijfrichting('r');
            }
            else if(hoeveel < 5){
                Schrijfrichting('&');
            }
            else{
                Schrijfrichting('x');
            }
        }
        if(a.gyro.y<-dode_hoek){
            if(hoeveel<2){
            Schrijfrichting('l');
            }
            else if(hoeveel < 5){
                Schrijfrichting('(');
            }
            else{
                Schrijfrichting('!');
            }
        }
    
}
