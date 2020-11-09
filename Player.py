import pygame as pg
import math
import random


class tank_data():
    def __init__(self,tank_x,tank_y,tank_angle,turret_angle): # Will be passed in a tuple. using * operator
        self.tank_x = tank_x
        self.tank_y = tank_y
        self.tank_angle = tank_angle
        self.turret_angle = turret_angle


class from_server_data():
    def __init__(self,tank_x,tank_y): # Will be passed in a tuple. using * operator
        self.tank_x = tank_x
        self.tank_y = tank_y
        self.tank_angle = 0
        self.turret_angle = 0

