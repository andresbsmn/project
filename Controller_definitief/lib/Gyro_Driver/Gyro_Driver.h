//later als functie klaar is   pin 6
#ifndef GYRO_DRIVER_H
#define GYRODRIVER_H
#include <Arduino.h>
#include <Adafruit_MPU6050.h>
const int dode_hoek = 2;
void gyro_ini();
void Schrijfrichting(char richting);
void gyro();

//int intToChar(int hoeveel);

#endif