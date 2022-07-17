# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 18:43:57 2018

@author: Wladimir
"""



class NozzlePosition(object):
    
    
    def __init__(self, x_pos = 0, y_pos = 0):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.coor = self.x_pos, self.y_pos
        
    
    #Setters are passed through here to check for valid entries
    def check(object):
        def wrapper(*args):
            try:
                # check the index of argument               
                if(not (isinstance(args[1], int))):
                    raise ValueError
            except:
                print("Error")
                while True:
                    n = input("Need Integer: ")
                    if n.isdigit():
                        n = int(n)
                        break
                return object(args[0], n) # args[0] is self
            return object(*args)
        return wrapper


    @property
    def x_pos(self):
        return self.__x_pos
    
    @x_pos.setter
    @check
    def x_pos(self, value):
        self.__x_pos = value
        
    @property
    def y_pos(self):
        return self.__y_pos

    @y_pos.setter
    @check  
    def y_pos(self, value):
        self.__y_pos = value
   
    @property
    def coor(self):
        return (self.__x_pos, self.__y_pos)
    
    
    @coor.setter
    def coor(self, tuple):
        self.__x_pos = tuple[0]
        self.__y_pos = tuple[1]

        



        