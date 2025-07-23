
from robot_hat import Robot,ADC,Servo,PWM,Pin
from robot_hat.utils import run_command
import time
from os import path, getlogin
import json
import math
import logging
import RPi.GPIO as GPIO

user_name = getlogin()
lowerthan_max = 1024
higherthan_min = 3072
adj = 500

# leftJoystick -> A0 (Lx), A1 (Ly), D0 (Lb)
# rightJoystick -> A2 (Rx), A3 (Ry), D1 (Rb)

class Joystick(ADC, Pin):
    """ Joystick Dual Module Class """

    def __init__(self, ch_x, ch_y, ch_b, address=None, *args, **kwargs):
        
        #super().__init__(ch_x, ch_y, ch_b, address, *args, **kwargs)
        #self.input = ADC(channel)
        self.ch_x = ch_x
        self.ch_y = ch_y
        self.ch_b = ch_b

        self.status_x = "None"
        self.status_y = "None"
        self.status_b = "None"

    def read_status_x(self):
        self.input = ADC(self.ch_x)
        status_x = self.input.read()
        logging.debug(f'ADC Status is: {status_x}')
        if(status_x < (lowerthan_max + adj)):
            self.status_x = "left"
        elif(status_x > (higherthan_min - adj)):
            self.status_x = "right"
        #else:
        #    self.status_y = "stall"
        return self.status_x
    
    def read_status_y(self):
        self.input = ADC(self.ch_y)
        status_y = self.input.read()
        logging.debug(f'ADC Status is: {status_y}')
        if(status_y < (lowerthan_max + adj)):
            #print(f'ADC STATUS: {status_y}')
            self.status_y = "down"
        elif(status_y > (higherthan_min - adj)):
            #print(f'ADC STATUS: {status_y}')
            self.status_y = "up"
        #else:
            # stop moving the arm
        #    self.status_y = "stall"
        return self.status_y

    def read_status_b(self):
        '''
        self.input = Pin(self.ch_b, mode=1, active_state=False)
        status_b = self.input.value()
        print("Check out digital values: ", status_b)
        if(status_b == 1):
            self.status_b = "pressed"
        '''
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ch_b, GPIO.IN)

        status_b = GPIO.input(self.ch_b)
        GPIO.cleanup()
        if not status_b:
            self.status_b = "pressed"
        else:
            self.status_b = "None"
        return self.status_b