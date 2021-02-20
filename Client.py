import pygame as pg
import math
import random
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
        self.turret_img = pg.image.load("images/tank/ACS_Tower_temp.png")
        
        self.img_top = self.turret_img
        self.img = self.tank_img
        self.turret_rect = self.turret_img.get_rect()
        self.rect = self.img.get_rect()
        self.rect.center = (start_xy) # Object starting place
        self.turret_rect.center = (self.rect.center)    # Useless. just for the calc func

        self.angle = 0
        self.speed = 4
        self.rotation_speed = 2
        self.turret_speed = 2
        self.turret_angle = 0

        self.active_bullets=[]

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

        #####
        self.screen_centered_tank = (int(screen_length / 2- self.rect[2]/2) ,int(screen_height / 2 -self.rect[3]/2))    # This is the pos for the tank to be in the center of the camera. This is defined here to prevent re-calc any frame
        self.screen_centered_turret =  (int(screen_length / 2 -self.turret_rect[2]/2),int(screen_height / 2 -self.turret_rect[3]/2))
        #####

    def shooting(self):
        key=pg.key.get_pressed()
        if key[pg.K_SPACE]:
            if len(self.active_bullets)==0:  # So you wont be able to double-shot
                data_to_send.a_bullet = (self.rect.center, self.turret_angle) # Adds the new bullet data to the server connection so it will drawn on the other players screen
                self.active_bullets.append(bullet(self.rect.center, self.turret_angle)) # Creates a bullet object to be shown in this player's screen

    def update(self):
        for self.a_bullet in self.active_bullets: # Updates the list of the active bullets
            if (self.a_bullet.isActive() == False):
                self.active_bullets.remove(self.a_bullet) # Removes the unactive bullets from the list


    def draw(self, screen_to_draw):
        
        for self.a_bullet in self.active_bullets: # draw all the player's bullets
            self.a_bullet.draw(screen_to_draw)
        
        screen_to_draw.blit(self.img, self.screen_centered_tank)  # Makes sure that the player will always be centered
        screen_to_draw.blit(self.img_top, self.screen_centered_turret)




class menu_bars():
    def __init__(self):

        self.myfont = pg.font.SysFont('Comic Sans MS', 15)

        self.money_bar_img=pg.image.load("images/ingameelements/Money Panel HUD.png")
        self.money_bar_pos= (30,0)
        self.money_bar_text = self.myfont.render(str(99), False, (255, 255, 255)) 

        self.health_bar_img = pg.image.load("images/ingameelements/healthbar.png")
        self.health_bar_text = self.myfont.render(str(99), False, (255, 255, 255)) 
        self.health_bar_pos= (30,550)
    
    def draw(self, screen_to_draw):   # Changes the text to the right amount of money to blit on the bar
        screen_to_draw.blit(self.money_bar_img, self.money_bar_pos)
        screen_to_draw.blit(self.money_bar_text, (50,5))  # Displays the health of the player

        screen_to_draw.blit(self.health_bar_img, self.health_bar_pos)
        screen_to_draw.blit(self.health_bar_text, (38+30,25+550))  # Displays the health of the player

class bullet():
    def __init__(self,start_xy,shooting_angle):
        self.bullet_animation_imgs = [pg.image.load("images/tankshot/ACS Fire1.png"), pg.image.load("images/tankshot/ACS Fire2.png"), pg.image.load("images/tankshot/ACS Fire3.png")]
        self.image = self.bullet_animation_imgs[0]   # Needs to be changed into animation
        self.rect = self.image.get_rect()
        self.angle = shooting_angle
        self.rect.center= (start_xy) # Object starting place
        self.bullet_speed=6
        self.image,self.rect = rot_center(self.image,self.rect,self.angle + 180) # Updates the photo to the new angle and sets the new center of the rect
    
    def isActive(self): # To test if it's on the screen or out
        if self.rect.center[0] > 0 and self.rect.center[0] < 5000 and self.rect.center[1] > 0 and self.rect.center[1] < 3000:  # If the bullet is out of the screen. numbers ain't good
            return True
        return False

    def draw(self, screen_to_draw):
        self.rect.center = calculate_new_xy (self.rect.center, self.bullet_speed, self.angle)   # Moves the bullet
        screen_to_draw.blit(self.image, (self.rect.center[0] - camera.offset[0], self.rect.center[1] - camera.offset[1]))  # Makes sure that the player will always be centered


class cameraClass():
    def __init__(self,start_pos):
        self.offset = [start_pos[0] - int(screen_length / 2),start_pos[1] - int(screen_height / 2)] # This is a list and not a tuple, because it needs to be changed

    def update(self, centered_object_to_follow):
        if centered_object_to_follow[0] > screen_length/2:
            self.offset[0] = centered_object_to_follow[0] - int(screen_length / 2)

        if centered_object_to_follow[1] > screen_height/2:
            self.offset[1] = centered_object_to_follow[1] - int(screen_height / 2)
  
class enemy():  # Just prints the enemy and his bullets to the screen as plain images
    def __init__(self,enemy_data):
        self.tank_img = pg.image.load("images/tank/movement/ACS_move._01.png")
        self.turret_img = pg.image.load("images/tank/ACS_Tower.png")

        self.tank_rect = self.tank_img.get_rect()
        self.tank_rect.center = (enemy_data.tank_x,enemy_data.tank_y) # Object starting place
        self.turret_rect = self.turret_img.get_rect()

        self.tank_img_rotated, self.tank_rect = rot_center(self.tank_img,self.tank_rect,enemy_data.tank_angle)
        self.turret_rect.center = (self.tank_rect.center)
        self.turret_img_rotated, self.turret_rect = rot_center(self.turret_img,self.turret_rect,enemy_data.turret_angle)
        
        self.enemy_active_bullets = []
        self.user_token = None

    
    def update(self,enemy_data):
        # Updates to new enemy pos by recieved data
        self.tank_rect.center = (enemy_data.tank_x,enemy_data.tank_y) # Object starting place
        self.tank_img_rotated, self.tank_rect = rot_center(self.tank_img,self.tank_rect,enemy_data.tank_angle)
        self.turret_rect.center = (self.tank_rect.center)
        self.turret_img_rotated, self.turret_rect = rot_center(self.turret_img,self.turret_rect,enemy_data.turret_angle)

        if enemy_data.a_bullet != None: # Checks for the shoot command in the recived data. this should happened once for each bullet
            self.enemy_active_bullets.append(bullet((enemy_data.tank_x,enemy_data.tank_y), enemy_data.turret_angle))
        
        for self.enemy_bullet in self.enemy_active_bullets: # Updates the list of the active bullets
            if (self.enemy_bullet.isActive() == False):
                self.enemy_active_bullets.remove(self.enemy_bullet) # Removes the unactive bullets from the list


    def draw(self):
        screen.blit(self.tank_img_rotated,(self.tank_rect[0] - camera.offset[0] ,self.tank_rect[1] - camera.offset[1]))   # Draws enemys on the screen, by the recieved data
        screen.blit(self.turret_img_rotated,(self.turret_rect[0] - camera.offset[0] ,self.turret_rect[1] - camera.offset[1]))   # Draws enemy's turret on the screen, by the recieved data

        if len(self.enemy_active_bullets) != 0:    # If there is an active bullet
            for self.enemy_bullet in self.enemy_active_bullets:
                self.enemy_bullet.draw(screen)


pg.init()   # Resets pygame libary
clock = pg.time.Clock() # Setting the clock

screen_height, screen_length =  600, 1100  # Those variables get used in the other moudles
screen = pg.display.set_mode(( screen_length, screen_height))      # Creating a window

pg.display.set_caption("Tanks", "Spine Runtime")  # Set window caption
pg.display.set_icon(pg.image.load("images/tankico.ico"))  # Set window icon image

running = True

n = network()
data_to_send = n.getP()
received_data = n.send(data_to_send)    # First connection made, gives back the stats data to be set

player = tank((1000,600))   # Creating an object from the tank class and adding it to the tank sprite group. It gets the starting point from the server

###########
menu_bars_obj = menu_bars()
camera = cameraClass(player.rect.center)
###########

background = pg.image.load("images/background2.png") # Loads the background image from the folder

all_enemys = [None] * 5 # A list of all the enemys in the game

while running:  # Main loop
    event = pg.event.poll()
    if event.type == pg.QUIT:  # Exit question
        running=False
    elif event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
            running = False  # Set running to False to end the while loop.
    

    screen.blit(background,(0 - camera.offset[0] ,0 - camera.offset[1]))

    camera.update(player.rect.center)

    ##################### Updates the data that is been sent to the server
    data_to_send.tank_x, data_to_send.tank_y = player.rect.center[0], player.rect.center[1]
    data_to_send.tank_angle = player.angle
    data_to_send.turret_angle = player.turret_angle
    data_to_send.user_token = 0
    #####################

    received_data = n.send(data_to_send)    # Sends the data while receiving new data


    for an_enemy in received_data:  # Creates new sprites of enemy according to the recieved list
        if all_enemys[an_enemy.user_token] == None: # Adds only missing enemys or new ones
            all_enemys[an_enemy.user_token] = enemy(an_enemy)
        else:
            all_enemys[an_enemy.user_token].update(an_enemy)
            all_enemys[an_enemy.user_token].draw()

    data_to_send.a_bullet = None

    player.movement()
    player.update()
    player.shooting()
    player.draw(screen)

    #############
    menu_bars_obj.draw(screen)
    #############
    pg.display.update()
    clock.tick(30)      # 60 FPS timer
