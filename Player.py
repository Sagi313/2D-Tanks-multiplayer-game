import pygame as pg
import math
import random


class tank_data():
    def __init__(self,tank_x,tank_y,tank_angle,turret_angle,user_token): # Will be passed in a tuple. using * operator
        self.tank_x = tank_x
        self.tank_y = tank_y
        self.tank_angle = tank_angle
        self.turret_angle = turret_angle
        self.a_bullet = None # Will hold a tuple, such as (bullet_x, bullet_y, bullet_angle). When no bullets are shot from *this* tank, this will hold a null value
        self.user_token = user_token