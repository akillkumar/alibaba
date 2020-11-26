'''
    CS-1340 Computer Networks
    Monsoon 2020
    
    Course Project
    @Authors: Akhil Kumar, Dhruv Khandelwal, Dhruva Panyam

    For now this is a simple echo server 
'''

import os
import sys
import socket
import random

from helper import *

def main ():
    # create client socket
    with socket.socket (socket.AF_INET, socket.SOCK_STREAM) as client:
        
        # connect to the server
        try:
            client.connect (server_addr)
            print (COLORS.green + "Connected to server" + COLORS.clear)
        except:
            print (COLORS.red + "Could not establish connection to server" + COLORS.clear)
            os._exit(1)

        # go through command line options to check if user wants to create a credential
        for arg in sys.argv:
            if "create" in arg:
                # first send the server signal
                client.sendall (SIG_CREATE.encode ())

                # get confirmation
                ack = client.recv (1024).decode()

                if ack == "-1":
                    print (COLORS.red + "Could not create credentials at the moment, please try again." + COLORS.clear)
                    return 

                # prompt user for id
                uID  = input ("Enter a username: " + COLORS.mag)
                print (COLORS.clear)

                # send this to server to verify
                client.sendall (uID.encode ())

                # get server ack
                ack = client.recv (1024).decode ()
                
                # if there is some error
                if not ack == "OK":
                    print (ack)
                    return
                
                '''
                    User credential generation
                    Simplified Feige-Fiat-Shamir identification scheme can be implemented here
                '''

                # generate two random primes
                p = gen ()
                q = gen ()

                # compute product of primes
                N = p * q

                # pick a random w
                w = random.randrange (N)

                # compute sqaure of w modulo n
                v = modexp (w, 2, N)
                print (v)

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
                print (confirmation)

                # write values to file to be able to log in later
                fp = open (uID+'.txt', 'w+')
                fp.write (str(w).rstrip('\n'))
                fp.write ('\n')
                fp.write (str(N).rstrip('\n'))
                fp.close ()
                return

        # if we are here it means the user wishes to log-in
        client.sendall (SIG_AUTH.encode ())

        # get confirmation
        ack = client.recv (1024).decode ()

        if ack == "-1":
            print (COLORS.red + "Could not log-in at the moment, please try again." + COLORS.clear)
            return 

        # get user input
        uID = input ("Enter your username: " + COLORS.mag)
        print (COLORS.clear)

        # send user ID to the server for verification
        client.sendall (uID.encode ())

        # get server ack
        ack = client.recv (1024).decode ()

        # if there is an error
        if not ack == "OK":
            print (ack)
            return

        '''
            This is where the ZKP magic happens
        '''
        # read our file for w and N
        # TODO command line option to provide path to credentials
        try:
            record = tuple(open(uID+".txt", "r"))
            w = int (record[0])
            N = int (record[1])
        except:
            print (COLORS.red + "Could not find credentials for " + uID + COLORS.clear)
            w = input ("Enter w: ")
            N = input ("Enter N: ")

        # pick a random number x between 1 and n
        # such that gcd (x, N) = 1
        x = 0
        while True:
            x = random.randrange (N)
            if gcd (x, N) == 1:
                break
        
        # compute y = x^2 mod N
        y = modexp (x, 2, N)

        print ("y =", y )

        # and send y to the server
        client.sendall (str(y).encode ())

        # server sends a random bit
        b = client.recv (4).decode ()

        # calculate z based on the bit 
        z = x * (w**int(b))
        print ("z =", z)

        # send z to the server
        client.sendall (str(z).encode ())

        # get confirmation
        confirmation = client.recv (1024).decode ()

        print (confirmation)
        
if __name__ == "__main__":
    main ()

