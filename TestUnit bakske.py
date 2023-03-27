import serial
import time
COM_POORT='COM7'


def vibrator():
    with serial.Serial(COM_POORT, 9600, timeout=1) as ser:
        ser.write(b'v')
def buzzer():
    with serial.Serial(COM_POORT, 9600, timeout=1) as ser:
        ser.write(b'b')


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
