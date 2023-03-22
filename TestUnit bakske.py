import serial
import time

def vibrator():
    ser = serial.Serial('COM9', 9600, timeout=1)  # open serial port
    ser.write(b'v')
    time.sleep(1)
    ser.write(b'0')
    ser.close()

def buzzer():
    ser = serial.Serial('COM9', 9600, timeout=1)  # open serial port  (com7 desktop Feniks,COM9 laptop Feniks)
    ser.write(b'b')
    time.sleep(1)
    ser.write(b'0')
    ser.close()


#e



for i in range(5):
    print(i)
print("Buzzer wordt geactiveerd! ")
buzzer()

print("buzzer deactiveerd")



for i in range(5):
    print(i)

print("vibrator active")
vibrator()

print("deactive ")