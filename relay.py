import RPi.GPIO as GPIO
import time

pin = 16
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin,GPIO.OUT)
GPIO.output(pin,False)

i=0
while i<2:
    i= i+1
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,True)
    time.sleep(1)
    GPIO.output(pin,False)
    time.sleep(2)
    print(i)

GPIO.cleanup()
