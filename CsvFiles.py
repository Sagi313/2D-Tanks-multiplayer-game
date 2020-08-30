import pygame as pg

win_height, win_length = 400, 800       # Window size parameters
screen = pg.display.set_mode((win_length, win_height))      # Creating a window
pg.display.set_caption("Tanks", "Spine Runtime")  # Set window caption
pg.display.set_icon(pg.image.load("tankico.ico"))  # Set window icon image



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

def animation(image,frames_amout,speed):
    rect= image.get_rect()
    list=[]
    for i in range (0,frames_amout):
        list[i]= (rect.x/frames_amout*i , 0)
    return list

image2=pg.image.load('TankAnimation.png')
print(animation(image2,10,5))
#while running:  # Main loop
#    event = pg.event.poll()
#    if event.type == pg.QUIT:  # Exit question
#        running=False

#    screen.fill((255,255,255))

#    pg.display.update()
#    clock.tick(30)      # 60 FPS timer