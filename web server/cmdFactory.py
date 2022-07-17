# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 14:23:20 2018

@author: reiswich

This class generates a list of commands for a full path and can work them
sequentially and in reverse order to generate an infinte loop (i.e. there will
always be a next command)
"""

from nozzlePos import NozzlePosition
from motorcom import MotorCommand
from math import ceil



class cmd_factory(NozzlePosition, MotorCommand):
    
    
    @staticmethod
    def vector_dif(tuple1, tuple2):
        return (tuple2[0] - tuple1[0], tuple2[1] - tuple1[1])
    
    
    def __init__(self, **kwargs):
        
        #initial state of mcom will be the first command!
        self.mcom = MotorCommand()
        self.mcom.dist = kwargs["length"]
        self.nos = NozzlePosition()
        
        
        self.width = kwargs["width"] #x coordinate
        self.spacing = kwargs["spacing"] #the spacing between rows
        self.length = kwargs["length"] #y coordinate
        
        self.layers = self.num_of_layers()
        self.positions = self.layers*2
        self.pos_list = self.get_positions()
        self.sequence = True #var that sets the back and forwards sequence
        

        

    @property
    def length(self):
        return self.__length

    @length.setter
    def length(self, value):
        self.__length = value

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        self.__width = value
        
    @property
    def spacing(self):
        return self.__spacing
    
    @spacing.setter
    def spacing(self, value):
        self.__spacing = value
        
    def num_of_layers(self):
        return int(ceil(self.width/self.spacing))
    
    
# =============================================================================
#       Generates a list of ordered coordinates. This has to be
#       called at the start, ONCE.
# =============================================================================
    def get_positions(self):
        a = [(0,0),(0,self.length)]
        for i in range(self.positions):
            dif_vector = self.vector_dif(a[i+1], a[i])
            
            if dif_vector[0] == 0:
                a.append((a[i+1][0] + self.spacing, a[i+1][1]))
            elif dif_vector[1] == 0:
                if a[i+1][1] == 0 :
                    a.append((a[i+1][0], a[i+1][1] + self.length))
                else:
                    a.append((a[i+1][0], a[i+1][1] - self.length))

        return a
    
# =============================================================================
#     Changes nozzle position according to last cmd
# =============================================================================
    def actualize_position(self):
        self.nos.coor = self.get_next_pos()
    
    
# =============================================================================
#     Returns the coordinate of next position
# =============================================================================
    def get_next_pos(self):
        if self.pos_list.index(self.nos.coor) == len(self.pos_list)-1:
            self.sequence = False
        elif self.pos_list.index(self.nos.coor) == 0:
            self.sequence = True
        
        if self.sequence:
            return self.pos_list[self.pos_list.index(self.nos.coor)+1]
        else:
            return self.pos_list[self.pos_list.index(self.nos.coor)-1]

    
    #if cmd received is old cmd, a new cmd is generated
    def command_getter(self, cmd):
        if self.mcom.get_command() == cmd :
            self.command_setter()
        
        #the first command is always the initial one of that instance!
        return self.mcom.get_command()
    
    def command_setter(self):
                
        self.actualize_position()
        
        move_vector = self.vector_dif((self.nos.coor), self.get_next_pos() )
        self.mcom.set_command(move_vector)
        

# =============================================================================
#      For testing purposes
# =============================================================================
if __name__ == "__main__":
    session = {"length" : 50 , "width" : 50, "spacing" : 20}
    a = cmd_factory(**session)
    cmd = 'ACK$'
    print(a.pos_list)
    print(a.command_getter(cmd))
#    for i in range(30):
#        cmd = a.command_getter(cmd)
#       
#        print(a.nos.coor)