# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 17:32:19 2019

@author: Wladimir
"""
import threading
from time import sleep, time
import serial
from serial.tools import list_ports
from cmdFactory import cmd_factory as cmd
from queue import Queue



class Serializer: 
    def __init__(self, width=5, length=5, spacing=2, time=20): 
        self.session = {"length" : length , "width" : width,\
                        "spacing" : spacing, "time" : time}
        self.arduino = serial.Serial(self.find_port(), 9600, timeout = .1)
        self.start_time = 0
        self.que = Queue()
        self.com = cmd(**self.in_steps(**self.session))
        
    
    @staticmethod
    def find_port():
        ports = list_ports.comports()
        p = str(ports[0])
        p = p.split(' ')
        print('found port:', p[0])
        return p[0]
    

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
                        #print(self.com.command_getter(data))
                        self.que.put(self.com.command_getter(data))
            except:
                break
                    
                    
    def sendD(self):
        #"%MYtFWDt50t$"
        sleep(.5)
        #self.arduino.write("ACK$".encode())
        self.arduino.write("ACK$".encode())
        sleep(.5)
        self.arduino.write("ACK$".encode())
        while True:
            print(self.session['time'] - int(time() - self.start_time))
            wdata = self.que.get()
            #print(wdata)
            
            try:
                self.arduino.write(wdata.encode())
            except:
                break
            if self.session['time'] <= int(time() - self.start_time):
                
                try:
                    self.arduino.write(b"END$")
                finally:
                    break
            sleep(.5)
        
        
    
    def main(self):    
        self.start_time = time()
        try:
            threads = []
            s = threading.Thread(target = self.sendD)
            s.daemon = True
            threads.append(s)
            s.start()
            t = threading.Thread(target = self.readD)
            t.daemon = True
            threads.append(t)
            t.start()
            
            threads[0].join()
            threads[1].join()
        finally:
            self.arduino.close()
            
            
    @staticmethod
    def in_steps(**kwargs):
        step = 10
        kwargs.pop("time")
        for val in kwargs:
            kwargs[val] = (kwargs[val] * step)
        return kwargs
        
    
    
if __name__ == "__main__":
    new = Serializer()
    new.main()
    