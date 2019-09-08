import RPi.GPIO as GPIO
import time
# Code for detecting button press for microswitch
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
if GPIO.input(5) == 0:
    print('button on')
elif GPIO.input(5) == 1:
    print('button off')
