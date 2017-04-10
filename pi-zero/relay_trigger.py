import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

try:
#GPIO.output(17,GPIO.HIGH)
        GPIO.output(27,GPIO.HIGH)
	time.sleep(0.5)
#GPIO.output(17,GPIO.LOW)
        GPIO.output(27,GPIO.LOW)
finally:
	GPIO.cleanup()

