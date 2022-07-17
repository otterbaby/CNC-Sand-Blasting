# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 17:45:27 2018

@author: Wladimir

The MotorCommand class implements the command structure of two stepper
motors. The get_command function returns a string of coded commands,
the set_command function interprets the command by receiving a vector.
"""
from enum import IntEnum


class MotorCommand(object):
    
    #integer values are chosen so that states can be flipped
    #by multiplying with -1
    class Motor(IntEnum):
        MX = -2
        MY = 2
        
    class Dir(IntEnum):
        FWD = 1
        BWD = -1
    
    FWD = Dir.FWD
    BWD = Dir.BWD
    MX = Motor.MX
    MY = Motor.MY

    keys = {MX : "MX" , MY : "MY" ,\
           FWD : "FWD" , BWD : "BWD"}
    
    
    def __init__(self, motor = MY, direc = FWD, dist = 0):
        #distance is measured in steps
        self.motor = motor
        self.direc = direc
        self.dist = dist
        self.vector = self.motor, self.direc, self.dist

    @property
    def motor(self):
        return self.__motor

    @motor.setter
    def motor(self, value):
        self.__motor = value

    @property
    def direc(self):
        return self.__direc

    @direc.setter
    def direc(self, value):
        self.__direc = value

    @property
    def dist(self):
        return self.__dist

    @dist.setter
    def dist(self, value):
        self.__dist = value
    
# =============================================================================
#     Receives a vector that indicates the direction of the next position.
#     Sets the motor to be activated next.
# =============================================================================
    def set_command(self, coord):
        if coord[0] == 0:
            self.motor = self.MY
            self.dist = abs(coord[1])
            if coord[1] < 0:
                self.direc = self.BWD
            else:
                self.direc = self.FWD
        
        elif coord[1] == 0:
            self.motor = self.MX
            self.dist = abs(coord[0])
            if coord[0] < 0:
                self.direc = self.BWD
            else:
                self.direc = self.FWD
                
        else:
            pass
        
# =============================================================================
#       Returns a string of the coded commands.
# =============================================================================
    def get_command(self):            
        comStr = '%' + MotorCommand.keys[self.motor] + 't' + \
        MotorCommand.keys[self.direc] + "t" + str(self.__dist) + "t$"
        return comStr
    
# =============================================================================
#     #This is for testing purposes!  
#     @property
#     def vector(self):
#         return self.motor, self.direc, self.dist
#     
#     #expects a tuple as parameter
#     @vector.setter
#     def vector(self, vector):
#         self.motor = vector[0]
#         self.direc = vector[1]
#         self.dist = vector[2]
# =============================================================================

if __name__ == "__main__":
    cmd = MotorCommand()
    
    cmd.set_command((0, -10))
    print(cmd.get_command())
        
    
