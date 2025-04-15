
from robot_hat import Robot,ADC,Servo,PWM
from robot_hat.utils import run_command
import time
from os import path, getlogin
import json
import math

user_name = getlogin()

class Joystick(ADC):
    """ Joystick Dual Module Class """

    def __init__(self, channel, address=None, *args, **kwargs):
        
        super().__init__(channel, address, *args, **kwargs)
        #self.input = ADC(channel)
        self.channel = channel
        self.status = "None"

    def read_status(self):
        self.input = ADC(self.channel)
        status = self.input.read()
        print(f'ADC Status is: {status}')
        if(status > 0):
            self.status = "up"
        return self.status
