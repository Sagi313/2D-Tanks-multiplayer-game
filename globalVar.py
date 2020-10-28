import mysql.connector
import pygame as pg

mydb= mysql.connector.connect(
            #user="sql7368261", 
            #password='FvpNYddSVE', 
            #host="sql7.freemysqlhosting.net	", 
            #port=3306, 
            #database='sql7368261',
            #ssl_disabled=True,

            user="root", 
            password='root', 
            host="localhost", 
            port=3306, 
            database='game',
            ssl_disabled= True,
                              ) # Connecting into MySQL DB that sits on an Azure cloud service

def get_user_info():
    my_cursor.execute("SELECT * FROM user_info WHERE user_id= '%d'" %user_id)
    user_info_temp=list(my_cursor.fetchall())    # Passes the returned tuple into a list
    my_cursor.execute("SELECT * FROM user_stats WHERE user_id= '%d'" %user_info_temp[0][0])
    user_stats_temp=list(my_cursor.fetchall())    # Passes the returned tuple into a list
    #my_cursor.execute("SELECT * FROM in_game WHERE user_id= '%d'" %user_info_temp[0][0])
    #in_game_temp=list(my_cursor.fetchall())    # Passes the returned tuple into a list
    global user_data
    user_data={'user_id' : user_info_temp[0][0],'user_name': user_info_temp[0][1], 'speed':user_stats_temp[0][3],'rotating_turret':user_stats_temp[0][2],'shooting_power':user_stats_temp[0][4],'exp':user_stats_temp[0][1] , 'health':user_info_temp[0][3]}


screen_height, screen_length =  600, 1100  # Those variables get used in the other moudles
pg.init()   # Resets pygame libary
user_id= 0   # Holds the user that is logged in the game ID's number
my_cursor=mydb.cursor() # Init the cursor




