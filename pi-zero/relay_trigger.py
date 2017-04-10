import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(10, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)

try:
	GPIO.output(10,GPIO.HIGH)
	GPIO.output(9,GPIO.HIGH)
	time.sleep(0.5)
finally:
	GPIO.cleanup()

