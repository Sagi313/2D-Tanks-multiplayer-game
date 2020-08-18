from tkinter import *
import csv

def sign_in_button_func(event): # Checks the data the user has entered
    with open('database.csv','r') as csv_file:  # Imports the csv file into a 'pointer'
        csv_reader = csv.reader(csv_file)

        for user in csv_reader:
            if user[0]== entry_username.get() and user[1] == entry_password.get():
                top.destroy()
                root.destroy()
                import PythonTest # Calls the game file

def cancel_button_func(): # A func that is exiting the program with the 'cancel' button
    print("It worked")
    top.destroy()
    root.destroy()
    sys.exit(0)

def register_button_func():
    print("It worked")
    with open('database.csv','a') as csv_file:  # Imports the csv file into a 'pointer'
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([entry_username.get(),entry_password.get()])
    print("It worked")

root= Tk()
top= Toplevel() 

top.geometry('800x400') # Setting the size of the login screen
top.title('Login screen') # Setting the window title
top.iconbitmap('tankico.ico')   # Setting the window tank icon

top.configure(background='white')
photo2=PhotoImage(file='TankPic.png') # Gets the image for the main logo
photo=Label(top,image=photo2,bg='white')
text_username=Label(top,text='Username: ',font={'Arial,14'})
entry_username=Entry(top) # The typing box
text_password=Label(top,text='Password: ',font={'Arial,14'})
entry_password=Entry(top,show="*")

cancel_button=Button(top,text='Cancel',command=lambda:cancel_button_func()) # A button to exit the program
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
cancel_button.pack()


root.withdraw()
root.mainloop()
