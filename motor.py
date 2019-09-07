#!/usr/bin/python
import RPi.GPIO as GPIO
import time

# Constants
DIR = 27
STEP = 22
SLEEP = 23
M0 = 24 #24 BCM
M1 = 25 #25 BCM
MIN_DELAY = 0.005 # 0.005
MOTOR_STEPS = 200
Button = 5 #BCM

# Initialise GPIO pins
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) #BCM
GPIO.setup(SLEEP,GPIO.OUT)
GPIO.setup(STEP,GPIO.OUT)
GPIO.setup(DIR,GPIO.OUT)
GPIO.setup(M0,GPIO.OUT)
GPIO.setup(M1,GPIO.OUT)
GPIO.setup(Button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Motor class
class Motor(object):
    def __init__(self):
        self.set_direction(1)
        self.set_step_type("full")
        self.disable()
        self.motor_steps = MOTOR_STEPS
        self.delay=MIN_DELAY
        self.speed = 60/(MIN_DELAY*2*self.motor_steps)
        self.set_speed(self.speed)
        GPIO.output(STEP,0)

    def enable(self):
        GPIO.output(SLEEP,1)
        self.enabled = 1

    def disable(self):
        GPIO.output(SLEEP,0)
        self.enabled=0

    def set_speed(self,rpm):
        self.delay = 60.0 / (rpm* self.motor_steps*2) # calculate delay (NB 2xdelay per step) change 20 back to 60
        self.speed = rpm

    def set_direction(self,d):
        self.direction = d
        GPIO.output(DIR,d)

    def set_step_type(self,type):
        if(type=="full"):
            GPIO.output(M0,0)
            GPIO.output(M1,0)
        elif(type=="micro-8"):
            GPIO.output(M0,1)
            GPIO.output(M1,1)

    def step(self):
        print("step")
        GPIO.output(STEP,1)
        time.sleep(self.delay)
        GPIO.output(STEP,0)
        time.sleep(self.delay)
        
    def steps(self,n=1):
        enable_toggle = ~self.enabled
        if(enable_toggle):
            self.enable()
            time.sleep(self.delay)

        self.enable()
        time.sleep(self.delay)

        # Set direction based on steps
        if(n==0):
            pass
        elif(n>0):
            self.set_direction(1)
        else:
            self.set_direction(0)

        print("Taking {} steps in direction ({})".format(abs(n),self.direction))

        GPIO.output(STEP,0)
        for i in range(abs(n)):
            self.step()
            
        if(enable_toggle):
            self.disable()    

    def dead_reckoning(self, bounce): #bounce depends on camera lens
        enable_toggle = ~self.enabled
        if(enable_toggle):
            self.enable()
            time.sleep(self.delay)

        self.enable()
        time.sleep(self.delay)

        # Set direction down towards dead reckoning
        self.set_direction(0)

        print("Undergoing dead reckoning")

        GPIO.output(STEP,0)
        for i in range(100000):
            self.step()
            if GPIO.input(Button) == 1: #Button is pressed, 'off'=0 (not pressed) 'on'=1 (pressed)
               print('Switch Hit') #Break out of steps with return statement
               break
        self.steps(bounce) #bounce back off of button to begin algorithm
        print('Dead Reckoning Complete')
        if(enable_toggle):
            self.disable()