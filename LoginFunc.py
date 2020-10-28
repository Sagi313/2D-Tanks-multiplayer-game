from tkinter import *
import globalVar
from  globalVar import *

def changing_screens(register_screen):
    if register_screen:
        sign_in_button.grid_forget()
        register_button.grid_forget()

        text_email.grid(row=3,column=0)
        entry_email.grid(row=3,column=1)
        text_age.grid(row=4,column=0)
        entry_age.grid(row=4,column=1)
        submit_button.grid(row=5,column=0)

    else:
        text_email.grid_forget()
        entry_email.grid_forget()
        text_age.grid_forget()
        entry_age.grid_forget()
        submit_button.grid_forget()

        sign_in_button.grid(row=3,column=0)
        register_button.grid(row=4,column=0)

def submit_button_func():
    sql_command = "INSERT INTO user_info (user_name ,password, email, age) VALUES (%s,%s,%s,%s)"
    info_query = (entry_username.get(), entry_password.get(), entry_email.get() , entry_age.get())
    my_cursor.execute(sql_command,info_query)

    sql_command2 = "INSERT INTO user_stats (user_id, speed, rotating_turret, shooting_power,exp) VALUES (%s,%s,%s,%s,%s)"
    info_query2 = (my_cursor.lastrowid, 4, 2, 1, 0)   # Setting the staring defualt values for this new user. A player starts from zero. His user_id is linked to the other table
    
    my_cursor.execute(sql_command2,info_query2)
    mydb.commit()
    
    changing_screens(0)
    text_log_result.config(text = "You have registered succsesfully")

def sign_in_button_func(event): # Checks the data the user has entered
    
    if entry_password.get() =="" or entry_username.get()=="":
        text_log_result.config(text= "Please enter username and password")
        return
    
    my_cursor.execute("SELECT * FROM user_info WHERE user_name= '%s' and password='%s'" %(entry_username.get(), entry_password.get())) # Checks if the entered password and user matches the databse
    users=list(my_cursor.fetchall())    # Passes the returned tuple into a list

    if len(users) > 0:  # Checks if there is a user that fits the arguments
        top.destroy() 
        root.destroy() 
        globalVar.user_id = users[0][0] # Aprroved login. sets the user_id to the globalVar
        print( globalVar.user_id)
    else:
        text_log_result.config(text= "Incorrect username or password")

def register_button_func():
    changing_screens(1)

def cancel_button_func(): # A func that is exiting the program with the 'cancel' button
    top.destroy()
    root.destroy()
    sys.exit(0)

def start_screen():
    entry_password.bind('<Return>',sign_in_button_func) 
    # Orginaze all the elements inside the window
    photo.grid(row=0,column=0,pady=50, padx=400, sticky=W+E,columnspan=2)
    text_username.grid(row=1,column=0)
    entry_username.grid(row=1,column=1)
    text_password.grid(row=2,column=0)
    entry_password.grid(row=2,column=1)
    sign_in_button.grid(row=3,column=0)
    register_button.grid(row=4,column=0)
    text_log_result.grid(row=5,column=0)

    exit_button.grid(row=6,column=0)

    root.withdraw()
    root.mainloop()

log_result=""
root= Tk( )
top= Toplevel() 

my_cursor = mydb.cursor() # Init the cursor

top.overrideredirect(0) # removes/sets the uppper window tool bar
top.geometry("%dx%d+0+0" % (screen_length, screen_height))   # Setting the size of the login screen

top.title('Login screen') # Setting the window title
top.iconbitmap('tankico.ico')   # Setting the window tank icon

logo_photos_img=PhotoImage(file='images/mainlogo.png') # Gets the image for the main logo

background_image2=PhotoImage(file='images/login/grass menu background.png')   # Sets the background image
background_label2 = Label(top, image=background_image2)
background_label2.place(x=0, y=0, relwidth=1, relheight=1)

background_image=PhotoImage(file='images/background.png')   # Sets the background image
background_label = Label(top, image=background_image)
background_label.place(x=screen_length/2-833/2, y=screen_height/2-434/2)    # Places the black square background in the center. needs to be changed to a formula withour the actual pixels of the photo

photo=Label(top,image=logo_photos_img,anchor = 'nw')
text_username=Label(top,text='Username: ',font={'Arial,14'})
entry_username=Entry(top) # The typing box
text_password=Label(top,text='Password: ',font={'Arial,14'})
entry_password=Entry(top,show="*")
text_log_result=Label(top,text=log_result,font={'Arial,14'})

text_email=Label(top,text='Email: ',font={'Arial,14'})
entry_email=Entry(top) # The typing box
text_age=Label(top,text='Age: ',font={'Arial,14'})
entry_age=Entry(top)

exit_button_img=PhotoImage(file='images/login/exit_button.png')
exit_button=Button(top,image=exit_button_img,command=lambda:cancel_button_func()) # A button to exit the program

register_button_img=PhotoImage(file='images/login/register_button.png')
register_button=Button(top, image = register_button_img, command=lambda:register_button_func()) # A button to register

sign_in_button_img=PhotoImage(file='images/login/login_button.png')
sign_in_button=Button(top,image=sign_in_button_img,command=lambda:sign_in_button_func('<Return>')) # A button to Sign in

submit_button_img=PhotoImage(file='images/login/submit_button.png')
submit_button=Button(top,image=submit_button_img,command=lambda:submit_button_func()) # A button to Sign in
