from tkinter import *
import mysql.connector

mydb= mysql.connector.connect(host='localhost',
                              user='root',
                              passwd='root',
                              database= 'testing_Data_Base',
                              ) # Connecting into MySQL DB

def sign_in_button_func(event): # Checks the data the user has entered
    my_cursor.execute("SELECT * FROM users_info WHERE name= '%s' and email='%s'" %(entry_username.get(), entry_password.get())) # Checks if the entered password and user matches the databse
    
    if entry_password.get() =="" or entry_username.get()=="":
        text_log_result.config(text= "Please enter username and password")
        return

    users=list(my_cursor.fetchall())    # Passes the returned tuple into a list
    
    if len(users) > 0:  # Checks if there is a user that fits the arguments
        top.destroy() 
        root.destroy() 
        import PythonTest # Calls the game file
    else:
        text_log_result.config(text= "Incorrect username or password")


def register_button_func():
    sql_command = "INSERT INTO users_info (name, email, age) VALUES (%s,%s,%s)"
    record1 = (entry_username.get(), entry_password.get(), 25)
    my_cursor.execute(sql_command,record1)
    mydb.commit()
    text_log_result.config(text= "You have registered succsesfully")


def cancel_button_func(): # A func that is exiting the program with the 'cancel' button
    top.destroy()
    root.destroy()
    sys.exit(0)


log_result=""
root= Tk()
top= Toplevel() 

my_cursor=mydb.cursor() # Init the cursor

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
top.overrideredirect(1) # removes the uppper window tool bar
top.geometry("%dx%d+0+0" % (w, h))   # Setting the size of the login screen

top.title('Login screen') # Setting the window title
top.iconbitmap('tankico.ico')   # Setting the window tank icon

top.configure(background='white')
photo2=PhotoImage(file='TankAnimation.png') # Gets the image for the main logo

#canvas = Canvas(root, width = 300, height = 300)      
#canvas.pack()      
##img = PhotoImage(file="TankPic")      
#canvas.create_image(20,20, anchor=NW, image=photo2)   

photo=Label(top,image=photo2,bg='white',width=460,anchor = 'nw')
text_username=Label(top,text='Username: ',font={'Arial,14'})
entry_username=Entry(top) # The typing box
text_password=Label(top,text='Password: ',font={'Arial,14'})
entry_password=Entry(top,show="*")
text_log_result=Label(top,text=log_result,font={'Arial,14'})


cancel_button=Button(top,text='Exit',command=lambda:cancel_button_func()) # A button to exit the program
register_button=Button(top,text='Register',command=lambda:register_button_func()) # A button to register
sign_in_button=Button(top,text='Sign In',command=lambda:sign_in_button_func('<Return>')) # A button to Sign in

entry_password.bind('<Return>',sign_in_button_func) 

# Orginaze all the elements inside thw window
photo.pack()
text_username.pack()
entry_username.pack()
text_password.pack()
entry_password.pack()
sign_in_button.pack()
register_button.pack()
text_log_result.pack()
cancel_button.pack()

root.withdraw()
root.mainloop()
