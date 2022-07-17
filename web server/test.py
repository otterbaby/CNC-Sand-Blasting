# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 19:10:12 2019

@author: Wladimir
"""

import serial
import serial.tools.list_ports
from motorcom import MotorCommand
from time import sleep

# =============================================================================
# Finds the port of Arduino
# =============================================================================
def find_port():

    ports = serial.tools.list_ports.comports()
    p = str(ports[0])
    p = p.split(' ')
       
    return p[0]

def set(tuple):
    mcom.set_command(tuple)

def transmit():
    print(mcom.get_command())
    arduino.write(mcom.get_command().encode())

if __name__ == "__main__":
    mcom = MotorCommand()
    set((0,-10))
    arduino = serial.Serial(find_port(), 9600, timeout = .1)
    transmit()
    sleep(.5)
    arduino.close()