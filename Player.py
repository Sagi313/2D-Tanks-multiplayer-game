import pygame as pg
import math
import random


class tank_data():
    def __init__(self,tank_x,tank_y,tank_angle,turret_angle): # Will be passed in a tuple. using * operator
        self.tank_x = tank_x
        self.tank_y = tank_y
        self.tank_angle = tank_angle
        self.turret_angle = turret_angle
        self.a_bullet = None # Will hold a tuple, such as (bullet_x, bullet_y, bullet_angle). When no bullets are shot from *this* tank, this will hold a null value

class static_data():
    def __inti__(self):
        self.exp = None
        self.user_id = None
        self.password = None
        self.username = None
        self.email = None
        self.age = None
        self.turret_speed = None
        self.tank_speed = None
        self.shooting_power = None
        self.command = None # Tells the server what to do. Buy upgrades, enter into a game and so
