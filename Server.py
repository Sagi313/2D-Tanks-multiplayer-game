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


players_list = [tank_data(200,200,0,0), tank_data(300,500,0,0), tank_data(500,500,0,0)]  # All the players data, stored into a list

def login_verification(client_info):    # Checks the data that was sent by the user and checks for it inside the DB. if he is registred, he gets his user_id
    my_cursor.execute("SELECT user_id FROM user_info WHERE user_name= '%s' and password='%s'" %client_info.username, client_info.password) # Checks if the entered password and user matches the databse
    users=list(my_cursor.fetchall())    # Passes the returned tuple into a list

    if len(users) > 0:  # Checks if there is a user that fits the arguments
        return users # User info matches the DB, he can enter. The func returns the user_id
    else:
        return 0

def register_to_DB(client_info):
    sql_command = "INSERT INTO user_info (user_name ,password, email, age) VALUES (%s,%s,%s,%s)"
    info_query = (client_info.user_name, client_info.password, client_info.email , client_info.age)
    my_cursor.execute(sql_command,info_query)

    sql_command2 = "INSERT INTO user_stats (user_id, speed, rotating_turret, shooting_power,exp) VALUES (%s,%s,%s,%s,%s)"
    info_query2 = (my_cursor.lastrowid, 4, 2, 1, 0)   # Setting the staring defualt values for this new user. A player starts from zero. His user_id is linked to the other table
    my_cursor.execute(sql_command2,info_query2)
    
    mydb.commit()   # Saves changes to the DB

def extract_user_data(my_user):
    my_cursor.execute("SELECT * FROM user_stats WHERE user_id= '%s'" %my_user.user_id) # Get's the user his stats from DB
    stats = list(my_cursor.fetchall())    # Passes the returned tuple into a list

    my_user.exp = stats[1]
    my_user.turret_speed = stats[2]
    my_user.tank_speed = stats[3]
    my_user.shooting_power = stats[4]
    my_user.command = None # Reset the command to Nothing. so the commands won't repeat

def client_commands(my_user):
    if my_user.command == 1:    # Upgrading turret speed
        if (my_user.exp > 10):   # Checks to see if your have enough "money"
            my_cursor.execute("UPDATE user_stats SET rotating_turret = '%s' , exp = '%s' WHERE user_id= '%s'" %my_user.turret_speed, my_user.exp-100, my_user.user_id) # Reduce the 'money' from the player in the DB, and upgrades his abillaty

    elif my_user.command == 2:    # Upgrading tank speed
        if (my_user.exp > 10):   # Checks to see if your have enough "money"
            my_cursor.execute("UPDATE user_stats SET speed = '%s' , exp = '%s' WHERE user_id= '%s'" %my_user.tank_speed, my_user.exp-100, my_user.user_id) # Reduce the 'money' from the player in the DB, and upgrades his abillaty

    elif my_user.command == 3:    # Upgrading shooting power
        if (my_user.exp > 10):   # Checks to see if your have enough "money"
            my_cursor.execute("UPDATE user_stats SET shooting_power = '%s' , exp = '%s' WHERE user_id= '%s'" %my_user.shooting_power, my_user.exp-100, my_user.user_id) # Reduce the 'money' from the player in the DB, and upgrades his abillaty

    elif my_user.command == 4:    # Enter the game
        pass

def threaded_client(conn, player_id):  # Connects a client and runs in the background using threading. as long as the player is connected, this func runs
    conn.sendall(pickle.dumps(players_list[player_id]))    # Gives the player his first data. Should be stats
    print("Sending : ", players_list[1])

    user_data = static_data()

    while user_data.user_id == None:    # First screen, getting usernames and passwords
        received_data = pickle.loads(conn.recv(2048))
        user_data.user_id = login_verification(received_data) # This func will check the given data to see if it fits the DB, and will change the user_id to the right one
        
        conn.sendall(pickle.dumps(user_data))
    
    while True: # As long as the user is on the grage screen
        received_data = pickle.loads(conn.recv(2048))
        extract_user_data(user_data)    # Updates the obj with the static data from DB
        client_commands(user_data)
        conn.sendall(pickle.dumps(user_data))


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


