import pygame as pg
import ctypes
import mysql.connector
import sys

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
        self.rect.topleft=(500,500) # Object starting place
        self.myfont = pg.font.SysFont('Comic Sans MS', 15)
    
    def update(self):   # Changes the text to the right amount of money to blit on the bar
        textsurface = self.myfont.render(str(player.health), False, (255, 255, 255))
        screen.blit(textsurface,self.rect.topleft)  # Displays the username of the player


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


def DB_info_getting(user_id):   # Takes the user's info to show on the screen
    my_cursor.execute("SELECT * FROM user_info WHERE user_id= '%s'" %user_id)
    users=list(my_cursor.fetchall())    # Passes the returned tuple into a list
    print (users[0][0])


def text_box(the_text):
        myfont = pg.font.SysFont('Comic Sans MS', 30)
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
        self.rect = (200,150)
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
    def __init__(self,element_to_upgrade,position,screen):
        pg.sprite.Sprite.__init__(self)
        self.upgrade_button_img= pg.image.load("images/login/plus upgrades.png")
        self.level_bar_img = pg.image.load("images/login/register_button.png")
        self.image = self.upgrade_button_img
        self.rect = self.image.get_rect()
        self.current_level = 3 #player.user_data[element_to_upgrade]
        self.screen=screen
        

    def update(self):  # If the button got clicked
        if event.type == pg.MOUSEBUTTONDOWN: # Set the x, y postions of the mouse click
            x, y = event.pos
            if self.rect.collidepoint(x, y):    # Checks if the mouse got pressed inside the Rect object
                self.current_level+=1

        for i in range(self.current_level): # Blits the amount of bars according to your current level. Should be called after bliting the background images
            self.screen.blit(self.level_bar_img,((10,10)))
            print(i)

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
                   import Game
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
        self.player_rank_img= pg.image.load("images/rankpic.png")
        self.image = self.player_rank_img
        self.rect = self.image.get_rect()
        self.rect.center = (100,100)

class player_stats():   # Takes all the user's info from the database, and sets it to an object
    def __init__(self):
        self.user_id=1
        my_cursor.execute("SELECT * FROM user_info WHERE user_id= '%d'" %self.user_id)
        user_info=list(my_cursor.fetchall())    # Passes the returned tuple into a list
        my_cursor.execute("SELECT * FROM user_stats WHERE user_id= '%d'" %user_info[0][0])
        user_stats=list(my_cursor.fetchall())    # Passes the returned tuple into a list
        self.user_data={'user_id' : self.user_id,'user_name': user_info[0][1], 'speed':user_stats[0][3],'rotating_turret':user_stats[0][2],'shooting_power':user_stats[0][4],'exp':user_stats[0][1] }

pg.init()   # Resets pygame libary

pg.display.set_caption("Tanks", "Spine Runtime")  # Set window caption
pg.display.set_icon(pg.image.load("tankico.ico"))  # Set window icon image

user32 = ctypes.windll.user32   # Gets the size of the user's screen. enables full screen
screen_height = user32.GetSystemMetrics(0)
screen_length =  user32.GetSystemMetrics(1)
screen = pg.display.set_mode((1100,600))   # Sets the full screen

your_tank = tank_animation()
static_sprites = pg.sprite.Group()
static_sprites.add(your_tank)
static_sprites.add(player_rank())
static_sprites.add(stats_bar())

button_group = pg.sprite.Group()
button_group.add(play_button())
button_group.add(logout_button())
button_group.add(upgrade_button(('speed'),(500,500),screen))

background = pg.image.load("images/login/grass menu background.png") # Loads the background image from the folder
#background = pg.transform.scale(background, (screen_height, screen_length)) # Changes the size of the folder to fit. This should be checked in other screens
menu_background_img = pg.image.load("images/background.png") # Loads the background image from the folder
my_cursor=mydb.cursor() # Init the cursor

DB_info_getting(1)
player= player_stats()

running = True
clock = pg.time.Clock() # Setting the clock

while running:  # Main loop
    event = pg.event.poll()
    if event.type == pg.QUIT:  # Exit question
        running=False
    elif event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
            running = False  # Set running to False to end the while loop.
    

    button_group.update()

    your_tank.update()
    screen.blit(background,(0,0))
    screen.blit(menu_background_img,(1100/2-832/2 ,600/2-434/2))

    screen.blit(text_box(player.user_data['user_name']),(0,0))  # Displays the username of the player
    #screen.fill((255,255,255))
    static_sprites.draw(screen)
    button_group.draw(screen)
  
    pg.display.update()
    clock.tick(15)      # 60 FPS timer