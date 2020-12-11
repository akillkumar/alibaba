'''
    CS-1340 Computer Networks
    Monsoon 2020
    
    Course Project
    @Authors: Akhil Kumar, Dhruv Khandelwal, Dhruva Panyam

    For now this is a simple echo server 
'''
import time
import os
import sys
import socket
import random
import json
from helper import *
from tkinter import *
import os
PORT = 9000
FORMAT = 'utf-8'
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def login_success():
    global login1_scrn
    login1_scrn=Toplevel(login_screen)
    login1_scrn.title("Login Success")
    login1_scrn.geometry("200x200")
    Label(login1_scrn,text="Login Success",fg="black").pack()
    Button(login1_scrn,text="ok",bg="black",fg="white",command=closebtn1).pack()
def reg_succ():
    global register_scrn 
    register_scrn=Toplevel(register_screen)
    register_scrn.title("Registration Successfull")
    register_scrn.geometry("200x200")
    Label(register_scrn,text="Registration Successfull", fg='black').pack()
    Button(register_scrn,text='ok',bg='black', fg='white', command=closebtn3).pack()

def reg_unsucc():
    global register_scrn1 
    register_scrn1=Toplevel(register_screen)
    register_scrn1.title("Registration Not Successfull")
    register_scrn1.geometry("200x200")
    Label(register_scrn1,text="ID already exits, try login page.", fg='black').pack()
    Button(register_scrn1,text='ok',bg='black', fg='white', command=closebtn4).pack()

def invalid_login():
    global invalid_screen
    invalid_screen=Toplevel(custom_cred_scrn)
    invalid_screen.title("Invalid Credentials")
    invalid_screen.geometry("200x200")
    Label(invalid_screen,text="Enter credentials are wrong.", fg='black').pack()
    Button(invalid_screen,text='ok',bg='black', fg='white', command=closebtn5).pack()

def custom_cred():
    global w1
    global w2
    global n1
    global n2
    global namer 
    global name4
    global custom_cred_scrn
    custom_cred_scrn=Toplevel(main_screen)
    custom_cred_scrn.title("Custom Credentials")
    custom_cred_scrn.geometry("300x250")
    Label(custom_cred_scrn,text="Enter Custom Credentials",height="2",width="300").pack()
    Label(text="").pack()
    Label(custom_cred_scrn,text="User Name:").pack()
    name4=StringVar()
    namer=Entry(custom_cred_scrn,textvariable=name4)
    namer.pack()
    Label(text="").pack()
    Label(custom_cred_scrn,text="Enter W").pack()
    w1=StringVar()
    w2=Entry(custom_cred_scrn,textvariable=w1)
    w2.pack()
    Label(custom_cred_scrn,text="Enter N").pack()
    n1=StringVar()
    n2=Entry(custom_cred_scrn,textvariable=n1)
    n2.pack()
    Button(custom_cred_scrn,text="ok",bg="black",fg="white",command=handle_custom).pack()


def user_not_found():
    global user_not_found_scrn
    user_not_found_scrn=Toplevel(login_screen)
    user_not_found_scrn.title("User Not Found")
    user_not_found_scrn.geometry("300x250")
    Label(text="").pack()
    Label(user_not_found_scrn,text="Unable to find user credentials. ").pack()
    Label(user_not_found_scrn,text="Enter custom credential from menu").pack()
    Button(user_not_found_scrn,text="ok",bg="black",fg="white",command=closebtn).pack()

def user_not_found1():
    global user_not_found_scrn1
    user_not_found_scrn1=Toplevel(custom_cred_scrn)
    user_not_found_scrn1.title("User Not Found")
    user_not_found_scrn1.geometry("300x250")
    Label(text="").pack()
    Label(user_not_found_scrn1,text="Unable to find user record ").pack()
    Label(user_not_found_scrn1,text="Please Register first.").pack()
    Button(user_not_found_scrn1,text="ok",bg="black",fg="white",command=closebtn6).pack()


def closebtn():
    user_not_found_scrn.destroy()
    login_screen.destroy()
    main_screen.destroy()

def closebtn1():
    login1_scrn.destroy()
    login_screen.destroy()
    main_screen.destroy()
    
def closebtn3():
    register_scrn.destroy()
    register_screen.destroy()
    main_screen.destroy()

def closebtn4():
    register_scrn1.destroy()
    register_screen.destroy()
    main_screen.destroy()

def closebtn5():
    invalid_screen.destroy()
    custom_cred_scrn.destroy()
    main_screen.destroy()

def closebtn6():
    user_not_found_scrn1.destroy()
    custom_cred_scrn.destroy()
    main_screen.destroy()
def login():
    global login_screen
    global name3
    global nam
    login_screen=Toplevel(main_screen)
    login_screen.title("Login Screen")
    login_screen.geometry("300x250")
    Label(login_screen,text="Login Screen",height="2",width="300").pack()
    Label(text="").pack()
    Label(login_screen,text="User Name *").pack()
    name3=StringVar()
    nam=Entry(login_screen,textvariable=name3)
    nam.pack()
    Button(login_screen,text="login",bg="black",fg="white",command=login_user).pack()

def login_user():
    uID = name3.get()
    uID=str(uID)
    client.sendall (SIG_AUTH.encode ())

    # get confirmation
    ack = client.recv (1024).decode ()

    if ack == "-1":
        print (COLORS.red + "Could not log-in at the moment, please try again." + COLORS.clear)
        return 0

    # send user ID to the server for verification
    client.send(uID.encode ())

    # get server ack
    ack = client.recv (1024).decode ()

    # if there is an error
    if not ack == "OK":
        user_not_found()
        return 0

    else:
        record = tuple(open(uID+".txt", "r"))
        w = int (record[0])
        N = int (record[1])
        print(COLORS.yell + 'Using secret values from ' + COLORS.mag + uID+'.txt' + COLORS.clear)
        print()

    '''
        This is where the ZKP magic happens
    '''
    # read our file for w and N
    # TODO command line option to provide path to credentials


    # pick a random number x between 1 and n
    # such that gcd (x, N) = 1
    x = [get_coprime(N) for _ in range(NUM_TRIALS)]
    
    # compute y = x^2 mod N
    y = [modexp (x[i], 2, N) for i in range(NUM_TRIALS)]

    # and send y to the server
    client.sendall (str(y).encode ())

    # server sends a random bit-string
    b = client.recv (1024).decode ()

    z = [x[i] * (w**int(b[i])) for i in range(NUM_TRIALS)]
    # calculate z based on the bit 
    # send z to the server
    client.sendall (str(z).encode ())

    # get confirmation
    confirmation = json.loads(client.recv (1024).decode ())
    print (confirmation['message'])
    login_success()
    if not confirmation['success']:
        user_not_found()


def handle_custom():          #this dont work idk whhyy
    uID = name4.get()
    uID=str(uID)
    client.sendall (SIG_AUTH.encode ())

    # get confirmation
    ack = client.recv (1024).decode ()

    if ack == "-1":
        print (COLORS.red + "Could not log-in at the moment, please try again." + COLORS.clear)
        return 0

    # send user ID to the server for verification
    client.send(uID.encode ())

    # get server ack
    ack = client.recv (1024).decode ()
    if not ack == "OK":
        user_not_found1()
        return 0
    w=int(w1.get())
    N=int(n1.get())
        # pick a random number x between 1 and n
    # such that gcd (x, N) = 1
    x = [get_coprime(N) for _ in range(NUM_TRIALS)]
    
    # compute y = x^2 mod N
    y = [modexp (x[i], 2, N) for i in range(NUM_TRIALS)]

    # and send y to the server
    client.sendall (str(y).encode ())

    # server sends a random bit-string
    b = client.recv (1024).decode ()

    z = [x[i] * (w**int(b[i])) for i in range(NUM_TRIALS)]
    # calculate z based on the bit 
    # send z to the server
    client.sendall (str(z).encode ())

    # get confirmation
    confirmation = json.loads(client.recv (1024).decode ())
    print (confirmation['message'])
    if confirmation['success']:
        login_success()
    if not confirmation['success']:
        print("Invalid Crentials")
        invalid_login()

def registration():
    global register_screen
    global name2
    register_screen=Toplevel(main_screen)
    register_screen.title("Registration Screen")
    register_screen.geometry("300x250")
    Label(register_screen,text="Registration Screen",height="2",width="300").pack()
    Label(text="").pack()
    Label(register_screen,text="User Name *").pack()
    global name
    name=StringVar()
    name2=Entry(register_screen,textvariable=name)
    name2.pack()
    Button(register_screen,text="Register",bg="black",fg="white",command=register_user).pack()

def register_user():
    name1=name.get()
    # first send the server signal
    client.sendall (SIG_CREATE.encode ())

    # get confirmation
    ack = client.recv (1024).decode()

    if ack == "-1":
        print (COLORS.red + "Could not create credentials at the moment, please try again." + COLORS.clear)
        return 0

    # prompt user for id
    uID  = name1
    print (COLORS.clear)

    # send this to server to verify
    client.sendall (uID.encode ())

    # get server ack
    ack = client.recv (1024).decode ()
    
    # if there is some error
    if not ack == "OK":
        print (ack)
        reg_unsucc()
    
    else:
        # generate two random primes
        p = gen ()
        q = gen ()

        # compute product of primes
        N = p * q

        # pick a random w
        w = random.randrange (N)

        # compute sqaure of w modulo n
        v = modexp (w, 2, N)

        # submit this to the server
        client.sendall (str(v).encode ())
        server_v = client.recv (2048).decode ()

        client.sendall (str(N).encode ())
        server_N = client.recv (2048).decode ()

        # make sure server has the same values
        try:
            if int (server_v) == v and int (server_N) == N:
                client.sendall ("OK".encode ())
            else:
                client.sendall ("ERR".encode ())
        except:
            pass

        # get creation confirmation from the server
        confirmation = client.recv (2048).decode ()
        reg_succ()
        print (confirmation)

        # write values to file to be able to log in later
        fp = open (uID+'.txt', 'w+')
        fp.write (str(w).rstrip('\n'))
        fp.write ('\n')
        fp.write (str(N).rstrip('\n'))
        fp.close ()
        return 0
    
def my_main_screen():
    global main_screen
    main_screen=Tk()
    main_screen.geometry("300x250")
    main_screen.title("Registration/login Screen")
    Label(text="  ", fg="white",height="2",width="300").pack()
    Button(text="Login",height="2",width="29",bg="black",fg="white", command=login).pack()
 
    Label(text="").pack()
    Button(text="Registration",height="2",width="30",bg="black",fg="white",command=registration).pack()
    Label(text="").pack()
    Button(text="Custom Credentials",height="2",width="30",bg="black",fg="white",command=custom_cred).pack()
    main_screen.mainloop()
my_main_screen()
    

       
        

 


