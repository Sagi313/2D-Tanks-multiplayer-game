import pygame as pg
import math
import random
import ctypes
from Network import network
from Player import *




def calculate_new_xy(old_xy,speed,current_angle):    # Gets the old pos and gives the new
    new_x = old_xy[0] + int(speed*math.cos(math.radians(90-current_angle))) # Caculating the new pos using right triangle. the int() is for rounding the numbers, because the screen can't hadle floats 
    new_y = old_xy[1] + int(speed*math.sin(math.radians(90-current_angle)))

    return new_x, new_y

def rot_center(image, rect, angle): # Rotating the image of the player and etc. rotate an image while keeping its center
        rot_image = pg.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)

        return rot_image,rot_rect

class tank():
    def __init__(self,start_xy):
        self.tank_img = pg.image.load("images/tank/movement/ACS_move._01.png")
        self.turret_img = pg.image.load("images/tank/ACS_Tower.png")
        
        self.img_top = self.turret_img
        self.img = self.tank_img
        self.turret_rect = self.turret_img.get_rect()
        self.rect = self.img.get_rect()
        self.rect.center = (start_xy) # Object starting place
        self.turret_rect.center = (self.rect.center)

        self.angle = 0
        self.speed = 4
        self.rotation_speed = 2
        self.turret_speed = 2
        self.turret_angle = 0

    def movement(self): # Takes the key from the arrows and moves the object
        key=pg.key.get_pressed()

        if key[pg.K_RIGHT]:
            self.angle-=self.rotation_speed
            self.angle%=360 # Makes sure the numbers won't get too big
            self.turret_angle-=self.turret_speed   # So the turret will move with the tank


        elif key[pg.K_LEFT]:
            self.angle+=self.rotation_speed
            self.angle%=360 # Makes sure the numbers won't get too big
            self.turret_angle+=self.turret_speed   # So the turret will move with the tank

        elif key[pg.K_UP]:
            self.rect.center=calculate_new_xy(self.rect.center,self.speed,self.angle)   # 15 degrees will fix the problem

        elif key[pg.K_DOWN]:
            self.rect.center=calculate_new_xy(self.rect.center,-self.speed,self.angle)
        
        if key[pg.K_z]:
            self.turret_angle+=self.turret_speed   # So the turret will move with the tank
        
        elif key[pg.K_x]:
            self.turret_angle-=self.turret_speed   # So the turret will move with the tank

        self.img, self.rect = rot_center(self.tank_img, self.rect, self.angle) # Updates the photo to the new angle and sets the new center of the rect
        self.img_top, self.turret_rect = rot_center(self.turret_img, self.turret_rect, self.turret_angle)

    def draw(self, screen_to_draw):
        screen_to_draw.blit(self.img, (int(screen_length / 2),int(screen_height / 2)))  # Makes sure that the player will always be centered
        screen_to_draw.blit(self.img_top, (int(screen_length / 2),int(screen_height / 2)))

class money_bar(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image=pg.image.load("images/ingameelements/Money Panel HUD.png")
        self.rect = self.image.get_rect()
        self.rect.topleft=(30,0) # Object starting place
        self.myfont = pg.font.SysFont('Comic Sans MS', 15)
    
    def update(self):   # Changes the text to the right amount of money to blit on the bar
        textsurface = self.myfont.render(str(99), False, (255, 255, 255)) 
        screen.blit(textsurface, tuple(map(sum, zip(self.rect.topleft, (30,4)))))  # Displays the current money (exp atm) of the player. The "tuple(map(sum, zip(z, b))))" is meant to sum 2 tuples, so the pos of the text will fit the bar

class health_bar(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image=pg.image.load("images/ingameelements/healthbar.png")
        self.rect = self.image.get_rect()
        self.rect.topleft=(30,550) # Object starting place
        self.myfont = pg.font.SysFont('Comic Sans MS', 15)
    
    def update(self):   # Changes the text to the right amount of money to blit on the bar
        textsurface = self.myfont.render(str(99), False, (255, 255, 255))
        screen.blit(textsurface, tuple(map(sum, zip(self.rect.topleft, (38,25)))))  # Displays the health of the player

class bullet(pg.sprite.Sprite):
    def __init__(self,start_xy,shooting_angle):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("images/tankshot/ACS Fire1.png")
        self.rect = self.image.get_rect()
        self.image,self.rect = rot_center(self.image,self.rect,self.angle+180) # Updates the photo to the new angle and sets the new center of the rect
        self.rect.center= (start_xy) # Object starting place
        self.angle = shooting_angle

class enemy(pg.sprite.Sprite):
    def __init__(self,start_xy):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("images/tank/movement/ACS_move._01.png")
        self.rect = self.image.get_rect()
        self.rect.center = (start_xy) # Object starting place
        self.angle = 0

class cameraClass():
    def __init__(self):
        self.offset = pg.Rect(600,1100,0,0)

    def update(self, centered_object_to_follow):
        if centered_object_to_follow[0] < screen_length/2:
            self.offset[2] = centered_object_to_follow[0]

        if centered_object_to_follow[1] < screen_height/2:
            self.offset[3] = centered_object_to_follow[1]
  

pg.init()   # Resets pygame libary
clock = pg.time.Clock() # Setting the clock

screen_height, screen_length =  600, 1100  # Those variables get used in the other moudles
screen = pg.display.set_mode(( screen_length,screen_height))      # Creating a window

pg.display.set_caption("Tanks", "Spine Runtime")  # Set window caption
pg.display.set_icon(pg.image.load("images/tankico.ico"))  # Set window icon image

running = True

n = network()
data_to_send = n.getP()
received_data = n.send(data_to_send)    # First connection made, gives back the stats data to be set
print(received_data)
bullets_group=pg.sprite.Group() # The tank's bullets that got fired

player = tank((200,200))   # Creating an object from the tank class and adding it to the tank sprite group. It gets the starting point from the server

###########
bars_and_panels=pg.sprite.Group()
bars_and_panels.add(money_bar())
bars_and_panels.add(health_bar())
###########
camera = cameraClass()

tank_img = pg.image.load("images/tank/movement/ACS_move._01.png")   # Used to test drawing images with blit
tank_rect = tank_img.get_rect()

background = pg.image.load("images/background2.png") # Loads the background image from the folder

while running:  # Main loop
    event = pg.event.poll()
    if event.type == pg.QUIT:  # Exit question
        running=False
    elif event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
            running = False  # Set running to False to end the while loop.
    

    screen.blit(background,(0 - camera.offset[2] ,0 - camera.offset[3]))

    camera.update(player.rect.center)

    #####################
    data_to_send.tank_x, data_to_send.tank_y = player.rect.center[0], player.rect.center[1]
    data_to_send.tank_angle = player.angle
    #####################

    received_data = n.send(data_to_send)    # Sends the data while receiving new data

    for an_enemy in received_data:  # Creates new sprites of enemy according to the recieved list
        tank_img_rotated, tank_rect = rot_center(tank_img,tank_img.get_rect(center=(an_enemy.tank_x,an_enemy.tank_y)),an_enemy.tank_angle)
        screen.blit(tank_img_rotated,(tank_rect[0] - camera.offset[2] ,tank_rect[1] - camera.offset[3]))   # Draws enemys on the screen, by the recieved data


    bullets_group.update()  # Moves the bullets that got shot

    player.movement()

    bullets_group.draw(screen)  # Draws the sprites of both groups on the screen of the game
    player.draw(screen)

    #############
    bars_and_panels.draw(screen)
    bars_and_panels.update()
    #############
    pg.display.update()
    clock.tick(30)      # 60 FPS timer
