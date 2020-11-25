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

                # TODO submit this to server
                client.sendall (str(v).encode ())
                server_v = client.recv (2048).decode ()

                client.sendall (str(N).encode ())
                server_N = client.recv (2048).decode ()

                try:
                    if int (server_v) == v and int (server_N) == N:
                        client.sendall ("OK".encode ())
                    else:
                        client.sendall ("ERR".encode ())
                except:
                    pass

                confirmation = client.recv (2048).decode ()
                print (confirmation)

        # if we are here it means the user wishes to log-in
        '''
            This is where the ZKP magic happens
        '''

        while True:
            client.sendall (input().encode())
            data = client.recv (2048).decode()
            print (data)

if __name__ == "__main__":
    main ()

