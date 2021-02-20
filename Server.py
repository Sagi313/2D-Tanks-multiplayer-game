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


