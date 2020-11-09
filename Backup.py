#import pygame as pg
#import math
#import random
#import ctypes
#from Network import network
#from Player import *




#def calculate_new_xy(old_xy,speed,current_angle):    # Gets the old pos and gives the new
#    new_x = old_xy[0] + int(speed*math.cos(math.radians(90-current_angle))) # Caculating the new pos using right triangle. the int() is for rounding the numbers, because the screen can't hadle floats 
#    new_y = old_xy[1] + int(speed*math.sin(math.radians(90-current_angle)))

#    return new_x, new_y

#def rot_center(image, rect, angle): # Rotating the image of the player and etc. rotate an image while keeping its center
#        rot_image = pg.transform.rotate(image, angle)
#        rot_rect = rot_image.get_rect(center=rect.center)

#        return rot_image,rot_rect

#class tank(pg.sprite.Sprite):
#    def __init__(self):
#        pg.sprite.Sprite.__init__(self)

#        self.image_index=0
#        self.tank_imgs=[]   #   Handling moving images
#        for i in range (1,5):   # Loads all the animation imgs into a list
#            self.tank_imgs.append(pg.image.load("images/tank/movement/ACS_move._0%d.png" %i))       # Might be useless. Very hard to notice the photo changing while moving
#        self.image = self.tank_imgs[self.image_index]
#        self.rect = self.image.get_rect()
#        self.rect.center=(300,200) # Object starting place


#    def movement(self): # Takes the key from the arrows and moves the object
#        key=pg.key.get_pressed()

#        if key[pg.K_RIGHT]:
#            player1.angle-=player1.rotation_speed
#            turret.angle-=player1.rotation_speed   # So the turret will move with the tank
#            player1.angle%=360 # Makes sure the numbers won't get too big

#        elif key[pg.K_LEFT]:
#            player1.angle+=player1.rotation_speed
#            turret.angle+=player1.rotation_speed   # So the turret will move with the tank
#            player1.angle%=360 # Makes sure the numbers won't get too big

#        elif key[pg.K_UP]:
#            self.rect.center=calculate_new_xy(self.rect.center,player1.speed,player1.angle)   # 15 degrees will fix the problem
#            self.image_index+=1 # Changing images by movement
#            self.image_index%=4

#        elif key[pg.K_DOWN]:
#            self.rect.center=calculate_new_xy(self.rect.center,-player1.speed,player1.angle)
#            self.image_index-=1 # Changing images by movement
#            self.image_index%=4

#        self.image = self.tank_imgs[self.image_index]   # Updating the right image
#        self.image,self.rect = rot_center(self.tank_imgs[self.image_index],self.rect,player1.angle) # Updates the photo to the new angle and sets the new center of the rect

#class money_bar(pg.sprite.Sprite):
#    def __init__(self):
#        pg.sprite.Sprite.__init__(self)
#        self.image=pg.image.load("images/ingameelements/Money Panel HUD.png")
#        self.rect = self.image.get_rect()
#        self.rect.topleft=(30,0) # Object starting place
#        self.myfont = pg.font.SysFont('Comic Sans MS', 15)
    
#    def update(self):   # Changes the text to the right amount of money to blit on the bar
#        textsurface = self.myfont.render(str(player1.exp), False, (255, 255, 255))
#        screen.blit(textsurface, tuple(map(sum, zip(self.rect.topleft, (30,4)))))  # Displays the current money (exp atm) of the player. The "tuple(map(sum, zip(z, b))))" is meant to sum 2 tuples, so the pos of the text will fit the bar

#class health_bar(pg.sprite.Sprite):
#    def __init__(self):
#        pg.sprite.Sprite.__init__(self)
#        self.image=pg.image.load("images/ingameelements/healthbar.png")
#        self.rect = self.image.get_rect()
#        self.rect.topleft=(30,550) # Object starting place
#        self.myfont = pg.font.SysFont('Comic Sans MS', 15)
    
#    def update(self):   # Changes the text to the right amount of money to blit on the bar
#        textsurface = self.myfont.render(str(player1.health), False, (255, 255, 255))
#        screen.blit(textsurface, tuple(map(sum, zip(self.rect.topleft, (38,25)))))  # Displays the health of the player

#class tank_turret(pg.sprite.Sprite):
#    def __init__(self):
#        pg.sprite.Sprite.__init__(self) 
#        self.turrent_img= pg.image.load("images/tank/ACS_Tower_temp.png")
#        self.image= self.turrent_img
#        self.rect = self.image.get_rect()
#        self.angle = player1.turret_angle

#        self.previous_time = pg.time.get_ticks()  # for the shoot() func. It sets the time for the shooting
#        self.shooting_rate = 500  # How many ticks you have to wait to shoot another shot

        
#    def update(self):
#        self.rect.center=player.rect.center # Sets the turret ontop on the tank
        
#        # Movement
#        key=pg.key.get_pressed()    

#        if key[pg.K_x]:
#            self.angle-= 4
#            self.angle%=360 # Makes sure the numbers won't get too big

#        elif key[pg.K_z]:
#            self.angle+= 4
#            self.angle%=360 # Makes sure the numbers won't get too big

#        self.image,self.rect = rot_center(self.turrent_img,self.rect,self.angle) # Updates the photo to the new angle and sets the new center of the rect
    
#    def shoot(self):    # Func that creates the bullet objects
#        key=pg.key.get_pressed()
#        current_time=pg.time.get_ticks()
        
#        if key[pg.K_SPACE] and current_time-self.previous_time>self.shooting_rate:  # Cannon balls
#            radius=70   # Length of the turret's barrel            
#            self.a_bullet = bullet(calculate_new_xy(self.rect.center,radius,self.angle),self.angle) # Start pos of the bullet is at the end of the barrel. using the same func as the moving with angle

#            bullets_group.add(self.a_bullet)
#            self.previous_time = current_time

#        if key[pg.K_LSHIFT] and current_time-self.previous_time>self.shooting_rate: # Land mines dropping
#            self.a_mine = land_mine(self.rect.center)
#            bullets_group.add(self.a_mine)
#            self.previous_time = current_time

#class bullet(pg.sprite.Sprite):
#    def __init__(self,start_xy,shooting_angle):
#        pg.sprite.Sprite.__init__(self)
#        self.angle= shooting_angle
#        self.tank_shot_imgs=[]
#        for i in range (1,4):   # Loads all the animation imgs into a list
#            self.tank_shot_imgs.append(pg.image.load("images/tankshot/ACS Fire%d.png" %i))        
#        self.frames_index=0
#        self.image = self.tank_shot_imgs[self.frames_index]
#        self.rect = self.image.get_rect()
#        self.image,self.rect = rot_center(self.tank_shot_imgs[self.frames_index],self.rect,self.angle+180) # Updates the photo to the new angle and sets the new center of the rect
#        self.rect.center= (start_xy) # Object starting place
#        self.speed=8
#        self.start_time = pg.time.get_ticks()   # The time when you make the shot. the object is created


#    def update(self):   # Override the 'update' func of the Group class of pygame.
#        self.rect.center = calculate_new_xy(self.rect.center,self.speed,self.angle) # Moves the object on the screen according to the angle and pos
#        if not screen.get_rect().contains(self.rect):   # Makes sure the object will end when exiting the screen limits
#            self.kill()
        
#        # Changes the bullet image to an animation using the time the object was created
#        self.current_time = pg.time.get_ticks()
#        self.since_shot= self.current_time - self.start_time
#        if (self.since_shot > (self.frames_index+1)*500):
#            if (self.frames_index > 2): # Deletes the object
#                self.kill()
#                return
#            self.image,self.rect = rot_center(self.tank_shot_imgs[self.frames_index],self.rect,self.angle+180) # Updates the photo to the new angle and sets the new center of the rect
#            self.frames_index+=1



#class land_mine(pg.sprite.Sprite):  # A bomb that stays in the tank's pos and waits a few sec before exploding
#    def __init__(self,start_xy):
#        pg.sprite.Sprite.__init__(self)
#        self.start_time = pg.time.get_ticks()   # The time when you drop the mine
#        self.land_mine_img= pg.image.load("images/tank/landminePic.png")
#        self.explosion_img=[]
#        for i in range (0,4):
#            self.explosion_img.append(pg.image.load("images/explosion/explode%d.png" %i))
        
#        self.image = self.land_mine_img
#        self.rect = self.image.get_rect()
#        self.rect.center = (start_xy)
#        self.frames_index=0

#    def update(self):   
#        self.current_time = pg.time.get_ticks()
#        self.since_shot= self.current_time- self.start_time
#        if (self.since_shot > 2000): # After 2000 ticks the image will change. The enemys will die
#            if (self.frames_index>3): # Deletes the object
#                self.kill()
#                return
#            self.image = self.explosion_img[self.frames_index]
#            self.frames_index+=1

#pg.init()   # Resets pygame libary
#clock = pg.time.Clock() # Setting the clock

#screen_height, screen_length =  600, 1100  # Those variables get used in the other moudles
#screen = pg.display.set_mode(( screen_length,screen_height))      # Creating a window

#pg.display.set_caption("Tanks", "Spine Runtime")  # Set window caption
#pg.display.set_icon(pg.image.load("images/tankico.ico"))  # Set window icon image

#running = True

#n = network()
#player1 = n.getP()

#bullets_group=pg.sprite.Group() # The tank's bullets that got fired
#player = tank()   # Creating an object from the tank class and adding it to the tank sprite group
#enemy = tank()   # Creating an object from the tank class and adding it to the tank sprite group

#turret=tank_turret()

#player.rect.center=(player1.x,player1.y)


#tanks_group = pg.sprite.Group()
#tanks_group.add(player)
#tanks_group.add(enemy)
#tanks_group.add(turret)

#bars_and_panels=pg.sprite.Group()
#bars_and_panels.add(money_bar())
#bars_and_panels.add(health_bar())

#background = pg.image.load("images/background2.png") # Loads the background image from the folder

#while running:  # Main loop
#    event = pg.event.poll()
#    if event.type == pg.QUIT:  # Exit question
#        running=False
#    elif event.type == pg.KEYDOWN:
#        if event.key == pg.K_ESCAPE:
#            running = False  # Set running to False to end the while loop.

#    player2 = n.send(player1)
#    enemy.rect.center=(player2.x,player2.y)


#    turret.shoot()  # The tank shooting func creates a bullet obj

#    bullets_group.update()  # Moves the bullets that got shot

#    player.movement()
#    player1.x, player1.y = player.rect.center[0], player.rect.center[1]

#    screen.blit(background,(0,0))

#    bullets_group.draw(screen)  # Draws the sprites of both groups on the screen of the game
#    tanks_group.draw(screen)
#    bars_and_panels.draw(screen)
#    bars_and_panels.update()
#    tanks_group.update()

#    pg.display.update()
#    clock.tick(30)      # 60 FPS timer
########################################################################
#import socket
#import pickle


#class network:
#    def __init__(self):
#        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        self.server = "10.0.0.3"    # My local ip adress. Using this, only machines that runs on my Local network can connect
#        self.port = 5555
#        self.addr = (self.server, self.port)
#        self.p = self.connect()

#    def getP(self):
#        return self.p

#    def connect(self):
#        try:
#            self.client.connect(self.addr)
#            return pickle.loads(self.client.recv(2048))
#        except:
#            pass

#    def send(self, data):
#        try:
#            self.client.send(pickle.dumps(data))
#            return pickle.loads(self.client.recv(2048))
#        except socket.error as e:
#            print(e)

#            ######################################################
#            import pygame as pg
#import math
#import random


#class tank_data():
#    def __init__(self,posx,posy):
#        self.x=posx
#        self.y=posy
#        self.health = 3
#        self.angle = 0
#        self.turret_angle=0
#        self.speed = 4
#        self.rotation_speed = 5
#        self.exp = 99
#        self.bulltes=[] # Each bullet is a tuple of (x,y,angle)


#########################################
#import socket
#from _thread import *
#from Player import tank_data
#import pickle

#server = "10.0.0.3"    # My local IP adress
#port = 5555

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#try:
#    s.bind((server, port))
#except socket.error as e:
#    str(e)

#s.listen(2) # Limits to 2 player
#print("Waiting for a connection, Server Started")


#players = [tank_data(100,100), tank_data(500,500)]  # All the players data, stored into a list

#def threaded_client(conn, player):  # Connects a client and runs in the background using threading. as long as the player is connected, this func runs
#    conn.send(pickle.dumps(players[player]))
#    reply = ""
#    while True:
#        try:
#            data = pickle.loads(conn.recv(2048))
#            players[player] = data  # Stores the recived data into the list, which is the DB

#            if not data:
#                print("Disconnected")
#                break
#            else:
#                if player == 1:
#                    reply = players[0]
#                else:
#                    reply = players[1]

#                print("Received: ", data)
#                print("Sending : ", reply)

#            conn.sendall(pickle.dumps(reply))
#        except:
#            break

#    print("Lost connection")
#    conn.close()

#currentPlayer = 0   # A counter that keeps track on how many users are logged in, and sets them with thier own number to connect
#while True:
#    conn, addr = s.accept()
#    print("Connected to:", addr)

#    start_new_thread(threaded_client, (conn, currentPlayer))
#    currentPlayer += 1



