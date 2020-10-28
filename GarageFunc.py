import pygame as pg
import ctypes
import mysql.connector
import sys

import globalVar
from globalVar import *

def text_box(the_text):
        myfont = pg.font.SysFont('Bahnschrift', 30)
        textsurface = myfont.render(the_text, False, (255, 255, 255))
        return textsurface

class tank_animation(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.animation_images=[]
        
        for i in range (0,8):  # A loop that loads all the images of the animation from the folder
            self.animation_images.append(pg.image.load("images/tankflash/TankAni%d.png" %i))

        self.image = self.animation_images[0]
        self.rect = self.image.get_rect()
        self.rect = (240,150)
        self.frames_index=0
    
    def update(self):
        self.current_time = pg.time.get_ticks()
        if self.current_time%100==0:
            self.frames_index=1
            return

        if self.frames_index > 0 and self.frames_index < 7:
            self.image = self.animation_images[self.frames_index]
            self.frames_index+=1
        else:
            self.frames_index=0
            self.image = self.animation_images[self.frames_index]

class upgrade_button(pg.sprite.Sprite): # A button to upgrade your speed/rotating/.., also, shows the right amount of bars according to your skills level
    def __init__(self,element_to_upgrade,position):
        pg.sprite.Sprite.__init__(self)
        self.upgrade_button_img= pg.image.load("images/login/plus upgrades.png")
        self.level_bar_img = pg.image.load("images/login/skill level bar.png")
        self.image = self.upgrade_button_img
        self.rect = self.image.get_rect()
        self.rect.center= position
        self.current_level = int(globalVar.user_data[element_to_upgrade] / 4) #  A level is 4 speed pixels
        self.element_to_upgrade=element_to_upgrade  # Hold this Var for the update func to use
        

    def update(self):  # If the button got clicked
        if event.type == pg.MOUSEBUTTONDOWN: # Set the x, y postions of the mouse click
            x, y = event.pos
            if self.rect.collidepoint(x, y):    # Checks if the mouse got pressed inside the Rect object
                self.current_level+=1

        for i in range(self.current_level): # Blits the amount of bars according to your current level. Should be called after bliting the background images
            screen.blit(self.level_bar_img,((self.rect.topleft[0] - 35 + 5*i, self.rect.topleft[1])))
            print(i)
        globalVar.user_data[self.element_to_upgrade] = self.current_level

class play_button(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.play_button_img= pg.image.load("images/login/play_button.png")
        self.image = self.play_button_img
        self.rect = self.image.get_rect()
        self.rect[0],self.rect[1] = 730,450 # Sets the button pos and keeping it in a Rect element. It only changes half of the tuple
    
    def update(self):  # If the button got clicked
        if event.type == pg.MOUSEBUTTONDOWN: # Set the x, y postions of the mouse click
            x, y = event.pos
            if self.rect.collidepoint(x, y):    # Checks if the mouse got pressed inside the Rect object
                   import GameFunc
                   sys.exit(0)

class stats_bar(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.stats_bar_img= pg.image.load("images/statsbarpic.png")
        self.image = self.stats_bar_img
        self.rect = self.image.get_rect()
        self.rect[0],self.rect[1]= 630 ,600/2-434/2 # Needs to be changed, so it will have variables, not pixels

class logout_button(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.logout_button_img= pg.image.load("images/login/logoutbutton.png")
        self.image = self.logout_button_img
        self.rect = self.image.get_rect()
        self.rect[0],self.rect[1]= 150 ,470 # Needs to be changed, so it will have variables, not pixels

class player_rank(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.exp_per_level= 100
        self.rank_level = globalVar.user_data['exp'] / self.exp_per_level # Get's the current level by the exp and the exp you need to level up
        self.player_rank_img= pg.image.load("images/ranks/%d.png" %self.rank_level)
        self.image = self.player_rank_img
        self.rect = self.image.get_rect()
        self.rect.center = (170,130)    # Places the image in the left corner of the menu. Might change to variables instead

def grage_screen():
    global screen   # Those vars are global so they can be used outside of this func
    global event
    screen = pg.display.set_mode((screen_length,screen_height),pg.DOUBLEBUF)   # Sets the screen with the right size. DOUBLEBUF disables the window resizig
    pg.display.set_caption("Tanks", "Spine Runtime")  # Set window caption
    pg.display.set_icon(pg.image.load("tankico.ico"))  # Set window icon image

    get_user_info() # This func is called once to get the user data to a dictonery from the DB. the func is found in GlobalVar.py

    your_tank = tank_animation()
    static_sprites = pg.sprite.Group()
    static_sprites.add(your_tank)
    static_sprites.add(player_rank())
    static_sprites.add(stats_bar())

    button_group = pg.sprite.Group()
    button_group.add(play_button())
    button_group.add(logout_button())
    button_group.add(upgrade_button(('speed'),(702,176)))   # Pos is on top of the stats bar

    background = pg.image.load("images/login/grass menu background.png") # Loads the background image from the folder
    menu_background_img = pg.image.load("images/background.png") # Loads the background image from the folder

    running = True
    clock = pg.time.Clock() # Setting the clock

    while running:  # Main loop
        event = pg.event.poll()
        if event.type == pg.QUIT:  # Exit question
            running=False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False  # Set running to False to end the while loop.
        
        screen.blit(background,(0,0))
        screen.blit(menu_background_img,(1100/2-832/2 ,600/2-434/2))


        your_tank.update()

        screen.blit(text_box(globalVar.user_data['user_name']),(150,150))  # Displays the username of the player
        static_sprites.draw(screen)
        button_group.draw(screen)
        button_group.update()   # Checks to see if the button got clicked. Also, blits some new images, so keep at the end

        pg.display.update()
        clock.tick(15)      # 15 FPS timer

