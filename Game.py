import pygame as pg
import math
import random
import ctypes
import mysql.connector


mydb= mysql.connector.connect(
            user="root", 
            password='root', 
            host="localhost", 
            port=3306, 
            database='Game',
            ssl_disabled=True,
                              ) # Connecting into MySQL DB that sits on an Azure cloud service

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
        screen.blit(textsurface,self.rect.topleft)  # Displays the username of the player

class health_bar(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image=pg.image.load("images/ingameelements/healthbar.png")
        self.rect = self.image.get_rect()
        self.rect.topleft=(30,550) # Object starting place
        self.myfont = pg.font.SysFont('Comic Sans MS', 15)
    
    def update(self):   # Changes the text to the right amount of money to blit on the bar
        textsurface = self.myfont.render(str(player.health), False, (255, 255, 255))
        screen.blit(textsurface,self.rect.topleft)  # Displays the health of the player


class tank(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.tank_img = pg.image.load("images/tank/ACS_Preview.png")
        self.image = self.tank_img
        self.rect = self.image.get_rect()
        self.rect.center=(300,200) # Object starting place

        #   Gets the data from the DB about the certain player using his uniqe user_id
        self.user_id = 1
        my_cursor.execute("SELECT * FROM user_stats WHERE user_id= '%d'" %self.user_id)
        user_stats=list(my_cursor.fetchall())    # Passes the returned tuple into a list

        self.angle = 0
        self.speed = user_stats[0][3]
        self.rotation_speed = user_stats[0][2]
        self.exp = user_stats[0][1]

        self.health = 3   # How many times do you need to get shot before you die
        self.shooting_rate = 500  # How many ticks you have to wait to shoot another shot
        self.previous_time = pg.time.get_ticks()  # for the shoot() func. It sets the time for the shooting


    
    def shoot(self):    # Func that creates the bullet objects
        key=pg.key.get_pressed()
        current_time=pg.time.get_ticks()
        if key[pg.K_SPACE] and current_time-self.previous_time>self.shooting_rate:  # Cannon balls
            self.a_bullet = bullet(self.rect.center,self.angle)
            bullets_group.add(self.a_bullet)
            self.previous_time = current_time

        if key[pg.K_LSHIFT] and current_time-self.previous_time>self.shooting_rate: # Land mines dropping
            self.a_mine = land_mine(self.rect.center)
            bullets_group.add(self.a_mine)
            self.previous_time = current_time



    def movement(self): # Takes the key from the arrows and moves the object
        key=pg.key.get_pressed()

        if key[pg.K_LEFT]:
            self.angle-=self.rotation_speed
            self.angle%=360 # Makes sure the numbers won't get too big

        elif key[pg.K_RIGHT]:
            self.angle+=self.rotation_speed
            self.angle%=360 # Makes sure the numbers won't get too big

        elif key[pg.K_UP]:
            self.rect.center=calculate_new_xy(self.rect.center,self.speed,self.angle)   # 15 degrees will fix the problem

        elif key[pg.K_DOWN]:
            self.rect.center=calculate_new_xy(self.rect.center,-self.speed,self.angle)

        self.image,self.rect = rot_center(self.tank_img,self.rect,self.angle) # Updates the photo to the new angle and sets the new center of the rect

class tank_turret(pg.sprite.Sprite):
    def __init__(self,tank_pos):
        pg.sprite.Sprite.__init__(self) 
        self.image=pg.image.load("images/tank/ACS_Tower.png")
        self.rect = self.image.get_rect()
        self.rect.center=tank_pos
    
    #def update(self):
    #    self.rect.center
   
class bullet(pg.sprite.Sprite):
    def __init__(self,start_xy,shooting_angle):
        pg.sprite.Sprite.__init__(self)
        self.angle= shooting_angle
        self.tank_shot_imgs=[]
        for i in range (1,4):   # Loads all the animation imgs into a list
            self.tank_shot_imgs.append(pg.image.load("images/tankshot/ACSF_0%d.png" %i))        
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
        if (self.since_shot > (self.frames_index+1)*800):
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

pg.init()   # Resets pygame libary
my_cursor=mydb.cursor() # Init the cursor


user32 = ctypes.windll.user32   # Gets the size of the screen of the user. enables full screen

clock = pg.time.Clock() # Setting the clock

win_height, win_length = user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)     # Window size parameters
screen = pg.display.set_mode(( 1100,600))      # Creating a window

pg.display.set_caption("Tanks", "Spine Runtime")  # Set window caption
pg.display.set_icon(pg.image.load("tankico.ico"))  # Set window icon image

running = True

bullets_group=pg.sprite.Group() # The tank's bullets that got fired
player = tank()   # Creating an object from the tank class and adding it to the tank sprite group
enemy = enemy_target()

tanks_group = pg.sprite.Group()
tanks_group.add(player)
tanks_group.add(enemy)

bars_and_panels=pg.sprite.Group() # The tank's bullets that got fired
bars_and_panels.add(money_bar())
bars_and_panels.add(health_bar())


background = pg.image.load("images/background2.png") # Loads the background image from the folder

while running:  # Main loop
    event = pg.event.poll()
    if event.type == pg.QUIT:  # Exit question
        running=False
    elif event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
            running = False  # Set running to False to end the while loop.

    screen.fill((255,255,255))

    player.movement()   # The tank's moving and rotating funcs
    player.shoot()  # The tank shooting func creates a bullet obj

    bullets_group.update()  # Moves the bullets that got shot
    
    for hit in pg.sprite.spritecollide(enemy,bullets_group,True,False): # Loops through the sprites that got hit with a shot. find collution
        enemy.hit()
    
    screen.blit(background,(0,0))

    bullets_group.draw(screen)  # Draws the sprites of both groups on the screen of the game
    tanks_group.draw(screen)
    bars_and_panels.draw(screen)
    bars_and_panels.update()

    pg.display.update()
    clock.tick(30)      # 60 FPS timer