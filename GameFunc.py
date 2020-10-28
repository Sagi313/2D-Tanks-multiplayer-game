import pygame as pg
import math
import random
import ctypes
import mysql.connector

import globalVar
from globalVar import *


def entering_DB():  # Setting the user who just logged inside the game to the database that stores all the in_game players
    sql_command = "INSERT INTO in_game (user_id ,health, x_axis, y_axis, turret_angle) VALUES (%s,%s,%s,%s,%s)"
    info_query = (globalVar.user_id, 100, 50,50 , 0)
    my_cursor.execute(sql_command,info_query)
    mydb.commit()

def updating_DB(health, x_axis, y_axis, turret_angle):  # Setting the user who just logged inside the game to the database that stores all the in_game players
    sql_command = "UPDATE in_game SET health= %s, x_axis = %s, y_axis= %s, turret_angle = %s WHERE user_id= %s"
    info_query = (health, x_axis, y_axis, turret_angle, globalVar.user_id)
    my_cursor.execute(sql_command,info_query)
    mydb.commit()


def getting_DB():   # Gets all the logged in users to paint on the screen
    my_cursor.execute("SELECT * FROM in_game WHERE user_id <> '%s'" %globalVar.user_id) # Checks if the entered password and user matches the databse
    users=list(my_cursor.fetchall())    # Passes the returned tuple into a list
    for user in users:
        
        pass

def calculate_new_xy(old_xy,speed,current_angle):    # Gets the old pos and gives the new
    new_x = old_xy[0] + int(speed*math.cos(math.radians(90-current_angle))) # Caculating the new pos using right triangle. the int() is for rounding the numbers, because the screen can't hadle floats 
    new_y = old_xy[1] + int(speed*math.sin(math.radians(90-current_angle)))

    return new_x, new_y

def rot_center(image, rect, angle): # Rotating the image of the player and etc. rotate an image while keeping its center
        rot_image = pg.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)

        return rot_image,rot_rect

class enemy_target(pg.sprite.Sprite):   # A class for a target tank who which is the enemy
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("images/tank/ACS_Preview.png")
        self.rect = self.image.get_rect()
        self.rect.center=(150,150) # Object starting place
        self.life = 3   # How many times do you need to get shot before you die
    
    def hit(self):  # When you get shot by the tank
        self.life-=1
        if self.life<=0:
            self.kill()

class money_bar(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image=pg.image.load("images/ingameelements/Money Panel HUD.png")
        self.rect = self.image.get_rect()
        self.rect.topleft=(30,0) # Object starting place
        self.myfont = pg.font.SysFont('Comic Sans MS', 15)
    
    def update(self):   # Changes the text to the right amount of money to blit on the bar
        textsurface = self.myfont.render(str(player.exp), False, (255, 255, 255))
        screen.blit(textsurface, tuple(map(sum, zip(self.rect.topleft, (30,4)))))  # Displays the current money (exp atm) of the player. The "tuple(map(sum, zip(z, b))))" is meant to sum 2 tuples, so the pos of the text will fit the bar

class health_bar(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image=pg.image.load("images/ingameelements/healthbar.png")
        self.rect = self.image.get_rect()
        self.rect.topleft=(30,550) # Object starting place
        self.myfont = pg.font.SysFont('Comic Sans MS', 15)
    
    def update(self):   # Changes the text to the right amount of money to blit on the bar
        textsurface = self.myfont.render(str(player.health), False, (255, 255, 255))
        screen.blit(textsurface, tuple(map(sum, zip(self.rect.topleft, (38,25)))))  # Displays the health of the player

class tank(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image_index=0
        self.tank_imgs=[]   #   Handling moving images
        for i in range (1,5):   # Loads all the animation imgs into a list
            self.tank_imgs.append(pg.image.load("images/tank/movement/ACS_move._0%d.png" %i))       # Might be useless. Very hard to notice the photo changing while moving
        self.image = self.tank_imgs[self.image_index]

        self.rect = self.image.get_rect()
        self.rect.center=(300,200) # Object starting place
        self.health = globalVar.user_data['health']   # How many times do you need to get shot before you die

        self.angle = 0
        self.speed = globalVar.user_data['speed']
        self.rotation_speed = globalVar.user_data['rotating_turret']
        self.exp = globalVar.user_data['exp']

    def movement(self): # Takes the key from the arrows and moves the object
        key=pg.key.get_pressed()

        if key[pg.K_RIGHT]:
            self.angle-=self.rotation_speed
            turret.angle-=self.rotation_speed   # So the turret will move with the tank
            self.angle%=360 # Makes sure the numbers won't get too big

        elif key[pg.K_LEFT]:
            self.angle+=self.rotation_speed
            turret.angle+=self.rotation_speed   # So the turret will move with the tank
            self.angle%=360 # Makes sure the numbers won't get too big

        elif key[pg.K_UP]:
            self.rect.center=calculate_new_xy(self.rect.center,self.speed,self.angle)   # 15 degrees will fix the problem
            self.image_index+=1 # Changing images by movement
            self.image_index%=4

        elif key[pg.K_DOWN]:
            self.rect.center=calculate_new_xy(self.rect.center,-self.speed,self.angle)
            self.image_index-=1 # Changing images by movement
            self.image_index%=4

        self.image = self.tank_imgs[self.image_index]   # Updating the right image
        self.image,self.rect = rot_center(self.tank_imgs[self.image_index],self.rect,self.angle) # Updates the photo to the new angle and sets the new center of the rect

class tank_turret(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self) 
        self.turrent_img= pg.image.load("images/tank/ACS_Tower_temp.png")
        self.image= self.turrent_img
        self.rect = self.image.get_rect()
        self.angle = player.angle

        self.previous_time = pg.time.get_ticks()  # for the shoot() func. It sets the time for the shooting
        self.shooting_rate = 500  # How many ticks you have to wait to shoot another shot

        
    def update(self):
        self.rect.center=player.rect.center # Sets the turret ontop on the tank
        
        # Movement
        key=pg.key.get_pressed()    

        if key[pg.K_x]:
            self.angle-= globalVar.user_data['rotating_turret']
            self.angle%=360 # Makes sure the numbers won't get too big

        elif key[pg.K_z]:
            self.angle+= globalVar.user_data['rotating_turret']
            self.angle%=360 # Makes sure the numbers won't get too big

        self.image,self.rect = rot_center(self.turrent_img,self.rect,self.angle) # Updates the photo to the new angle and sets the new center of the rect
    
    def shoot(self):    # Func that creates the bullet objects
        key=pg.key.get_pressed()
        current_time=pg.time.get_ticks()
        
        if key[pg.K_SPACE] and current_time-self.previous_time>self.shooting_rate:  # Cannon balls
            radius=70   # Length of the turret's barrel            
            self.a_bullet = bullet(calculate_new_xy(self.rect.center,radius,self.angle),self.angle) # Start pos of the bullet is at the end of the barrel. using the same func as the moving with angle

            bullets_group.add(self.a_bullet)
            self.previous_time = current_time

        if key[pg.K_LSHIFT] and current_time-self.previous_time>self.shooting_rate: # Land mines dropping
            self.a_mine = land_mine(self.rect.center)
            bullets_group.add(self.a_mine)
            self.previous_time = current_time


class bullet(pg.sprite.Sprite):
    def __init__(self,start_xy,shooting_angle):
        pg.sprite.Sprite.__init__(self)
        self.angle= shooting_angle
        self.tank_shot_imgs=[]
        for i in range (1,4):   # Loads all the animation imgs into a list
            self.tank_shot_imgs.append(pg.image.load("images/tankshot/ACS Fire%d.png" %i))        
        self.frames_index=0
        self.image = self.tank_shot_imgs[self.frames_index]
        self.rect = self.image.get_rect()
        self.image,self.rect = rot_center(self.tank_shot_imgs[self.frames_index],self.rect,self.angle+180) # Updates the photo to the new angle and sets the new center of the rect
        self.rect.center= (start_xy) # Object starting place
        self.speed=8
        self.start_time = pg.time.get_ticks()   # The time when you make the shot. the object is created


    def update(self):   # Override the 'update' func of the Group class of pygame.
        self.rect.center = calculate_new_xy(self.rect.center,self.speed,self.angle) # Moves the object on the screen according to the angle and pos
        if not screen.get_rect().contains(self.rect):   # Makes sure the object will end when exiting the screen limits
            self.kill()
        
        # Changes the bullet image to an animation using the time the object was created
        self.current_time = pg.time.get_ticks()
        self.since_shot= self.current_time - self.start_time
        if (self.since_shot > (self.frames_index+1)*500):
            if (self.frames_index > 2): # Deletes the object
                self.kill()
                return
            self.image,self.rect = rot_center(self.tank_shot_imgs[self.frames_index],self.rect,self.angle+180) # Updates the photo to the new angle and sets the new center of the rect
            self.frames_index+=1

class land_mine(pg.sprite.Sprite):  # A bomb that stays in the tank's pos and waits a few sec before exploding
    def __init__(self,start_xy):
        pg.sprite.Sprite.__init__(self)
        self.start_time = pg.time.get_ticks()   # The time when you drop the mine
        self.land_mine_img= pg.image.load("images/tank/landminePic.png")
        self.explosion_img=[]
        for i in range (0,4):
            self.explosion_img.append(pg.image.load("images/explosion/explode%d.png" %i))
        
        self.image = self.land_mine_img
        self.rect = self.image.get_rect()
        self.rect.center = (start_xy)
        self.frames_index=0

    def update(self):   
        self.current_time = pg.time.get_ticks()
        self.since_shot= self.current_time- self.start_time
        if (self.since_shot > 2000): # After 2000 ticks the image will change. The enemys will die
            if (self.frames_index>3): # Deletes the object
                self.kill()
                return
            self.image = self.explosion_img[self.frames_index]
            self.frames_index+=1

my_cursor=mydb.cursor() # Init the cursor

clock = pg.time.Clock() # Setting the clock

screen = pg.display.set_mode(( screen_length,screen_height))      # Creating a window

pg.display.set_caption("Tanks", "Spine Runtime")  # Set window caption
pg.display.set_icon(pg.image.load("tankico.ico"))  # Set window icon image

running = True

bullets_group=pg.sprite.Group() # The tank's bullets that got fired
player = tank()   # Creating an object from the tank class and adding it to the tank sprite group
enemy = enemy_target()
turret=tank_turret()

tanks_group = pg.sprite.Group()
tanks_group.add(player)
tanks_group.add(turret)
tanks_group.add(enemy)

bars_and_panels=pg.sprite.Group() # The tank's bullets that got fired
bars_and_panels.add(money_bar())
bars_and_panels.add(health_bar())

background = pg.image.load("images/background2.png") # Loads the background image from the folder

#entering_DB()  # Commented untill there will be a func that deletes the player from the DB when exiting

while running:  # Main loop
    event = pg.event.poll()
    if event.type == pg.QUIT:  # Exit question
        running=False
    elif event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
            running = False  # Set running to False to end the while loop.


    player.movement()   # The tank's moving and rotating funcs
    turret.shoot()  # The tank shooting func creates a bullet obj

    bullets_group.update()  # Moves the bullets that got shot
    
    for hit in pg.sprite.spritecollide(enemy,bullets_group,True,False): # Loops through the sprites that got hit with a shot. find collution
        enemy.hit()
    
    screen.blit(background,(0,0))

    bullets_group.draw(screen)  # Draws the sprites of both groups on the screen of the game
    tanks_group.draw(screen)
    bars_and_panels.draw(screen)
    bars_and_panels.update()
    tanks_group.update()

    updating_DB(globalVar.user_data['health'] ,player.rect.center[0],player.rect.center[1],player.angle)    # Sets all the current values of pos and stats to the in_game DB

    pg.display.update()
    clock.tick(30)      # 60 FPS timer