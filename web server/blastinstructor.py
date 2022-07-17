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


            
            
def readD():
    while arduino.is_open:
        try:
            if (arduino.in_waiting > 0):
                data = arduino.readline().decode()                
                data.strip()
                print(data)
                if (data == 'END$'):
                    break
                else:
                    que.put(cmd.command_getter(data))
        except:
            break
                
                
def sendD():
    arduino.write(b"ACK$")
    sleep(.5)
    while True:
        wdata = que.get()
        
        try:
            arduino.write(wdata.encode())
        except:
            break
        if session["time"] <= int(time() - start_time):
            que.get()
            try:
                arduino.write(b"END$")
            finally:
                break
        sleep(.5)
        print(int(time() - start_time))

# =============================================================================
# Receives distance in mm and converts into steps.
# =============================================================================
def in_steps(**kwargs):
    step = 10
    kwargs.pop("time")
    for val in kwargs:
        kwargs[val] = (kwargs[val] * step)
    return kwargs


# =============================================================================
# Setting up send and receive threads
# =============================================================================
def main():    
    try:
        threads = []
        t = threading.Thread(target = readD)
        t.daemon = True
        threads.append(t)
        t.start()
        s = threading.Thread(target = sendD)
        s.daemon = True
        threads.append(s)
        s.start()
        threads[0].join()
        threads[1].join()
    finally:
        arduino.close()
        print(f'Elapsed Time {time()-start_time}' )
        print("Port closed!")
        
        
# =============================================================================
# Finds the port of Arduino
# =============================================================================
def find_port():
    ports = list_ports.comports()
    p = str(ports[0])
    p = p.split(' ')
    return p[0]

# =============================================================================
# External input
# =============================================================================
if __name__ == "blastinstructor":
    print(f'external')
    arduino = serial.Serial(find_port(), 9600, timeout = .1)
    sleep(.5)
    que = Queue()
    session = {"length" : 0 , "width" : 0, "spacing" : 0, "time" : 0}
    for key in session:
        try:
            session[key] = int(input(f"Enter the {key}: "))
        except:
            while True:
                session[key] = input("Please enter a valid integer.")
                if session[key].isdigit():
                            session[key] = int(session[key])
                            break

    cmd = cmd(**in_steps(**session))
    start_time = time()
    main()
    
# =============================================================================
# Setting up all global variables and initialzing serial communication
# =============================================================================
if __name__ == "__main__":
    arduino = serial.Serial(find_port(), 9600, timeout = .1)
    sleep(.5)
    que = Queue()
    session = {"length" : 0 , "width" : 0, "spacing" : 0, "time" : 0}
    for key in session:
        try:
            session[key] = int(input(f"Enter the {key}: "))
        except:
            while True:
                session[key] = input("Please eneter a valid integer.")
                if session[key].isdigit():
                            session[key] = int(session[key])
                            break

    cmd = cmd(**in_steps(**session))
    start_time = time()
    main()
