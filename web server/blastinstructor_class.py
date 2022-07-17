# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import serial
import threading
from cmdFactory import cmd_factory as cmd
from time import sleep, time
from queue import Queue
from serial.tools import list_ports

class blast:
    
    def __init__(self, width, length, spacing, time):
        self.que = Queue()
        self.session = {"length" : length , "width" : width,\
                        "spacing" : spacing, "time" : time}
        self.cmd = cmd(**self.in_steps(**self.session))
        print(self.cmd.pos_list)
        self.arduino = serial.Serial(self.find_port(), 9600, timeout = .1)
        sleep(.5)
        self.start_time = 0

            
    def readD(self):
        while self.arduino.is_open:
            sleep(.5)
            try:
                if (self.arduino.in_waiting > 0):
                    data = self.arduino.readline().decode()                
                    data.strip()
                    print(data)
                    if (data == 'END$'):
                        break
                    else:
                        self.que.put(self.cmd.command_getter(data))
            except:
                break
                    
                    
    def sendD(self):
        self.arduino.write(b"ACK$")
        sleep(.5)
        self.arduino.write(b"ACK$")
        sleep(.5)
        while True:
            wdata = self.que.get()
            try:
                self.arduino.write(wdata.encode())
            except:
                break
            if self.session["time"] <= int(time() - self.start_time):
                self.que.get()
                try:
                    self.arduino.write(b"END$")
                finally:
                    break
            sleep(.5)
            
    
    # =============================================================================
    # Receives distance in mm and converts into steps.
    # =============================================================================
    @staticmethod
    def in_steps(**kwargs):
        step = 10
        kwargs.pop("time")
        for val in kwargs:
            kwargs[val] = (kwargs[val] * step)
        return kwargs
    
    
    # =============================================================================
    # Finds the port of Arduino
    # =============================================================================
    @staticmethod
    def find_port():
        ports = list_ports.comports()
        p = str(ports[0])
        p = p.split(' ')
        print('found port ', p[0])
        return p[0]
    
    
    # =============================================================================
    # Setting up send and receive threads
    # =============================================================================
    def main(self):
        self.start_time = time()
        try:
            threads = []
            t = threading.Thread(target = self.readD)
            t.daemon = True
            threads.append(t)
            t.start()
            s = threading.Thread(target = self.sendD)
            s.daemon = True
            threads.append(s)
            s.start()
            threads[0].join()
            threads[1].join()
        finally:
            self.arduino.close()
            print(f'Elapsed Time {time()-self.start_time}' )
            print("Port closed!")
            
    
    
    
# =============================================================================
# Setting up all global variables and initialzing serial communication
# =============================================================================
if __name__ == "__main__":
    s = {"length" : 0 , "width" : 0, "spacing" : 0, "time" : 0}
    for key in s:
        try:
            s[key] = int(input(f"Enter the {key}: "))
        except:
            while True:
                s[key] = input("Please eneter a valid integer.")
                if s[key].isdigit():
                            s[key] = int(s[key])
                            break
    new = blast(s['length'],s['width'],s['spacing'],s['time'])
    new.main()
