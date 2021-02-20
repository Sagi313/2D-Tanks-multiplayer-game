from tkinter import *
from Player import *

def sign_in_button_func(event):
    if entry_password.get() =="" or entry_username.get()=="":
        static_canvas.itemconfigure(text_log_result,text= "Please enter username and password")
        return
    else:
        my_data = static_data()
        my_data.username = entry_username.get()
        my_data.password = entry_password.get()
        return my_data
        

def register_button_func():
    pass

def submit_button_func():
    pass

def log_in_screen():
    screen.mainloop()

screen_height, screen_length =  600, 1100  # Those variables get used in the other moudles
screen= Tk( )
screen.geometry("%dx%d+0+0" % (screen_length, screen_height))   # Setting the size of the login screen

static_canvas = Canvas (screen, width = screen_length, height = screen_height) # All static objects. images backgrounds and etc.

### Image Importing ###
main_logo_img=PhotoImage(file='images/mainlogo.png')
sign_in_button_img=PhotoImage(file='images/login/login_button.png')
submit_button_img=PhotoImage(file='images/login/submit_button.png')
register_button_img=PhotoImage(file='images/login/register_button.png')
exit_button_img=PhotoImage(file='images/login/exit_button.png')
black_square_img =PhotoImage(file='images/background.png')   # Sets the background image
background_img=PhotoImage(file='images/login/grass menu background.png')   # Sets the background image
#######################

background = static_canvas.create_image((0,0),anchor = "nw", image = background_img)    # Grass background
black_square = static_canvas.create_image((screen_length/2,310), image = black_square_img)  # The black square in the center. everything is ontop of this
main_logo = static_canvas.create_image((screen_length/2,50) ,image = main_logo_img)

sign_in_button = Button(static_canvas,image=sign_in_button_img,command=lambda:sign_in_button_func('<Return>')) # A button to Sign in
button1_window = static_canvas.create_window(10, 10, anchor=NW, window=sign_in_button)

text_username= static_canvas.create_text(300,300,text='Username: ',font={'Arial,14'}, fill = "white")   # Text on canvas with transparent bg
text_password= static_canvas.create_text(300,350,text='Password: ',font={'Arial,14'}, fill = "white")   # Text on canvas with transparent bg
text_log_result = static_canvas.create_text(400,450,text='None',font={'Arial,14'}, fill = "white")


entry_username=Entry(static_canvas) # The typing box
entry_password=Entry(static_canvas,show="*")

static_canvas.place(x=0,y=0)
entry_username.place(x=350,y=300)
entry_password.place(x=350,y=350)

