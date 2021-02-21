import socket
from _thread import *
from Player import *
import pickle
import pygame as pg


server = socket.gethostname()    # My local IP adress
port = 5555

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen(3) # Limits to x player
print("Server Started, Waiting for a connection...")


players_list = [tank_data(200,200,0,0,1), tank_data(300,500,0,0,2), tank_data(500,500,0,0,3)]  # All the players data, stored into a list
active_bullets = []    # Used in the trackingBullets()

def trackingBullets():
    # Checks for new bullets 
    for player in players_list:
        if player.a_bullet != None: # a player shot his bullet
            active_bullets.append(Bullet((player.tank_x,player.tank_y),player.turret_angle))
    
    for a_bullet in active_bullets:
        if (a_bullet.isActive()):
            a_bullet.move()
        else:
            active_bullets.remove(a_bullet)

def detecteCollusion(): # To see if a bullet hits a player
    self.tank_img = pg.image.load("images/tank/movement/ACS_move._01.png")
    self.tank_rect = self.tank_img.get_rect()
    for a_player in players_list:
        for a_bullet in active_bullets:
            if a_player.colliderect(a_bullet):
                print("Hit!")

class Bullet():
    def __init__(self,start_xy,shooting_angle):
        self.bullet_img = pg.image.load("images/tankshot/ACS Fire1.png") # Might need to be changed into a circle, not this image
        self.image = self.bullet_img   
        self.rect = self.image.get_rect()
        self.angle = shooting_angle
        self.rect.center = (start_xy) # Object starting place
        self.bullet_speed = 6
    
    def move(self):
        self.rect.center = calculate_new_xy (self.rect.center, self.bullet_speed, self.angle)   # Moves the bullet

    def isActive(self): # To test if it's on the screen or out
        if self.rect.center[0] > 0 and self.rect.center[0] < 5000 and self.rect.center[1] > 0 and self.rect.center[1] < 3000:  # If the bullet is out of the screen. numbers ain't good
            return True
        return False


def threaded_client(conn, player_id):  # Connects a client and runs in the background using threading. as long as the player is connected, this func runs
    conn.sendall(pickle.dumps(players_list[player_id]))    # Gives the player his first data. Should be stats
    print("Sending : ", players_list[1])

    reply = ""
    while True:
        try:
            received_data = pickle.loads(conn.recv(2048))
            players_list[player_id] = received_data  # Stores the recived data into the list, which is the DB

            if not received_data:
                print("Disconnected")
                break
            else:
                reply = players_list[:player_id] + players_list[player_id + 1:] # Sets the list of all players to be sent. sends all except the client that is connected
                print("Received: ", received_data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break
    

    print("Lost connection")
    conn.close()

currentPlayer = 0   # A counter that keeps track on how many users are logged in, and sets them with thier own number to connect
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    if currentPlayer <= 3: # Limit's the amount of players in the server. should be the same number as listed in the "Listen" func
        start_new_thread(threaded_client, (conn, currentPlayer))
        currentPlayer += 1


