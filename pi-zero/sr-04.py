import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG = 14
ECHO = 15

TRIG = 23
ECHO = 18

print "Distance measurement in progress"

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)

print "Waiting for sensor to settle"
time.sleep(2)

# trigger pulse
GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)

pulse_start = None
while GPIO.input(ECHO) == 0:
    pulse_start = time.time()

pulse_end = None
while GPIO.input(ECHO) == 1:
    pulse_end = time.time()

pulse_duration = pulse_end - pulse_start


distance = 17150 * pulse_duration # d = vt where v =speed of sound

print "Distance", distance*0.393701 , "in"

GPIO.cleanup()

