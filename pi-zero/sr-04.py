import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)

# What we use to determine open or closed
DISTANCE_THRESHOLD = 9.75

TRIG = 14
ECHO = 15

# Right side
TRIG = 23
ECHO = 18

# Setup pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)

# Wait for sensor to settle
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

try:
    pulse_duration = pulse_end - pulse_start
except TypeError:
    # This means we could not measure so most likely garage is down. Return high duration
    # which will signify closed
    pass
    pulse_duration = 1.0

distance = 17150 * pulse_duration # d = vt where v =speed of sound
distance *= 0.393701
exit_code = None

if distance > DISTANCE_THRESHOLD:
    print ("CLOSED {0:.2f} in".format(distance))
    exit_code = 0
else:
    print ("OPEN {0:.2f} in".format(distance))
    exit_code = 2

GPIO.cleanup()
sys.exit(exit_code)
