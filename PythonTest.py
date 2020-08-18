import pygame as pg
import math
import random


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
        self.image = pg.image.load("enemyTankpic.png")
        self.rect = self.image.get_rect()
        self.rect.center=(150,150) # Object starting place
        self.life = 3   # How many times do you need to get shot before you die
    
    def hit(self):  # When you get shot by the tank
        self.life-=1
        if self.life<=0:
            self.kill()



class tank(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.tank_img = pg.image.load("TankPic.png")
        self.image = self.tank_img
        self.rect = self.image.get_rect()
        self.rect.center=(300,200) # Object starting place
        self.angle = 0
        self.speed = 4
        self.rotation_speed=1;
        self.life = 3   # How many times do you need to get shot before you die
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

    
   
class bullet(pg.sprite.Sprite):
    def __init__(self,start_xy,shooting_angle):
        pg.sprite.Sprite.__init__(self)
        self.bullet_img = pg.image.load("CannonBall.png")
        self.image = self.bullet_img
        self.rect = self.image.get_rect()
        self.rect.center= (start_xy) # Object starting place
        self.angle= shooting_angle
        self.speed=6

    def update(self):   # Override the 'update' func of the Group class of pygame.
        self.rect.center = calculate_new_xy(self.rect.center,self.speed,self.angle)
        if not screen.get_rect().contains(self.rect):
            self.speed*=-1
            #self.kill()

class land_mine(pg.sprite.Sprite):  # A bomb that stays in the tank's pos and waits a few sec before exploding
    def __init__(self,start_xy):
        pg.sprite.Sprite.__init__(self)
        self.start_time = pg.time.get_ticks()   # The time when you drop the mine
        self.land_mine_img= pg.image.load("landminePic.png")
        self.explosion_img = pg.image.load("boomPic.png")
        self.image = self.land_mine_img
        self.rect = self.image.get_rect()
        self.rect.center = (start_xy)

    def update(self):   
        self.current_time = pg.time.get_ticks()
        if (self.current_time- self.start_time > 1800): # After 1800 ticks the image will change. The enemys will die
            self.image = self.explosion_img
        if (self.current_time- self.start_time > 5000): # Deletes the object
            self.kill()



clock = pg.time.Clock() # Setting the clock

win_height, win_length = 400, 800       # Window size parameters
screen = pg.display.set_mode((win_length, win_height))      # Creating a window
pg.display.set_caption("Tanks", "Spine Runtime")  # Set window caption
pg.display.set_icon(pg.image.load("tankico.ico"))  # Set window icon image

running = True

bullets_group=pg.sprite.Group() # The tank's bullets that got fired
player = tank()   # Creating an object from the tank class and adding it to the tank sprite group
enemy = enemy_target()

tanks_group = pg.sprite.Group()
tanks_group.add(player)
tanks_group.add(enemy)


while running:  # Main loop
    event = pg.event.poll()
    if event.type == pg.QUIT:  # Exit question
        running=False

    screen.fill((255,255,255))

    player.movement()   # The tank's moving and rotating funcs
    player.shoot()  # The tank shooting func creates a bullet obj

    bullets_group.update()  # Moves the bullets that got shot
    
    for hit in pg.sprite.spritecollide(enemy,bullets_group,True,False): # Loops through the sprites that got hit with a shot. find collution
        enemy.hit()
    

    bullets_group.draw(screen)  # Draws the sprites of both groups on the screen of the game
    tanks_group.draw(screen)

    pg.display.update()
    clock.tick(30)      # 60 FPS timer