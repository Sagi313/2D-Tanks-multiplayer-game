import socket
from _thread import *
from Player import *
import pickle
import mysql.connector
import pygame as pg

mydb= mysql.connector.connect(
            user="root", 
            password='root', 
            host="localhost", 
            port=3306, 
            database='game',
            ssl_disabled= True,)    # Connecting into MySQL DB that sits on an Azure cloud service

my_cursor=mydb.cursor() # Init the cursor

server = socket.gethostname()    # My local IP adress
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(3) # Limits to x player
print("Server Started, Waiting for a connection...")


players_list = [tank_data(122,111,0,0), tank_data(300,300,0,0), tank_data(500,500,0,0)]  # All the players data, stored into a list

def login_verification(client_info):    # Checks the data that was sent by the user and checks for it inside the DB. if he is registred, he gets his user_id
    my_cursor.execute("SELECT user_id FROM user_info WHERE user_name= '%s' and password='%s'" %client_info.user_name, client_info.password) # Checks if the entered password and user matches the databse
    users=list(my_cursor.fetchall())    # Passes the returned tuple into a list

    if len(users) > 0:  # Checks if there is a user that fits the arguments
        return users # User info matches the DB, he can enter. The func returns the user_id
    else:
        return 0



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

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1


