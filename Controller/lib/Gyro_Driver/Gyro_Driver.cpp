
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



void Schrijfrichting(char richting, char hoeveel){
    if(richting == 'l'){
        //stuur links
        Keyboard.press('l');
        delay(100);
        Keyboard.release('l');
    }
    if(richting == 'r'){
        //stuur rechts
        Keyboard.press('r');
        delay(100);
        Keyboard.release('r');
    }
        Keyboard.press(hoeveel);
        delay(100);
        Keyboard.release(hoeveel);
    }

void gyro(){//pos y-as is rechts g.gyro.y
    // if(mpu.getMotionInterruptStatus()) {}
        sensors_event_t a, g, temp;
        mpu.getEvent(&a, &g, &temp);
        int hoeveel = round((a.gyro.y));//max values +-250=> 9*(gyrowaarde/250)  = gyrowaarde/28; 5 experimentele waardepppppppppppppppppppppppppppppppppppppppppppppppppppp
        if(hoeveel>=10){hoeveel = 9;}
        char hoeveel_char = intToChar(hoeveel);
        if(a.gyro.y>dode_hoek){
            Schrijfrichting('r',hoeveel_char);
            // SerialUSB.print(a.gyro.y);
        }
        if(a.gyro.y<-dode_hoek){
            Schrijfrichting('l',hoeveel_char);
            // SerialUSB.print(a.gyro.y);
        }
    
}
int intToChar(int hoeveel){
    if(hoeveel<0){hoeveel = -hoeveel;}
    char hoeveel_char = '?';
        switch (hoeveel){//https://stackoverflow.com/a/4629196
            case 0:hoeveel_char = '0'; break;
            case 1:hoeveel_char = '1'; break;
            case 2:hoeveel_char = '2';break;
            case 3:hoeveel_char = '3';break;
            case 4:hoeveel_char = '4';break;
            case 5:hoeveel_char = '5';break;
            case 6:hoeveel_char = '6';break;
            case 7:hoeveel_char = '7';break;
            case 8:hoeveel_char = '8';break;
            case 9:hoeveel_char = '9';break;
            default:hoeveel_char = '?';break;
        }
        return hoeveel_char;
}
