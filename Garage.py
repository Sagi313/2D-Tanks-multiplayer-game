import pygame as pg
import ctypes


class tank_animation(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.land_mine_img= pg.image.load("landminePic.png")
        self.animation_images=[]
        for i in range (0,10):
            self.animation_images.append(pg.image.load("images/tankflash/%d.png" %i))
        self.image = self.animation_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (300,350)
        self.frames_index=0
    
    def update(self):
        self.current_time = pg.time.get_ticks()
        if self.current_time%100==0:
            self.frames_index=1
            return

        if self.frames_index > 0 and self.frames_index < 9:
            self.image = self.animation_images[self.frames_index]
            self.frames_index+=1
        else:
            self.frames_index=0
            self.image = self.animation_images[self.frames_index]






user32 = ctypes.windll.user32
screen_height = user32.GetSystemMetrics(0)
screen_length =  user32.GetSystemMetrics(1)
screen = pg.display.set_mode((screen_height,screen_length),pg.FULLSCREEN)

your_tank = tank_animation()
static_sprites = pg.sprite.Group()
static_sprites.add(your_tank)


running = True
clock = pg.time.Clock() # Setting the clock

while running:  # Main loop
    event = pg.event.poll()
    if event.type == pg.QUIT:  # Exit question
        running=False
    elif event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
            running = False  # Set running to False to end the while loop.

    your_tank.update()
    screen.fill((255,255,255))
    static_sprites.draw(screen)
  
    pg.display.update()
    clock.tick(15)      # 60 FPS timer