'''
    CS-1340 Computer Networks
    Monsoon 2020
    
    Course Project
    @Authors: Akhil Kumar, Dhruv Khandelwal, Dhruva Panyam

    For now this is a simple echo server 
'''

import os
import json
import socket

from helper import *

# create a socket
with socket.socket (socket.AF_INET, socket.SOCK_STREAM) as server:
    # bind to an IP, port
    server.bind (server_addr)

    # listen on the port
    server.listen (1)
    print (COLORS.blue + "Server running. Listening on", server_addr[0] + ":" + str(server_addr[1]) + COLORS.clear)
    
    while True:
        # accept client connection
        # get client socket object and address
        connection, client_addr = server.accept ()

        # if we have a valid connection
        if connection:
            print (COLORS.green + "Connected to client", client_addr, COLORS.clear)

            # first message from client will be either a 1 or a 0 to indicate the activity
            # 0 - user credential creation
            # 1 - user authentication
            choice = connection.recv (1024).decode ()

            if choice == SIG_CREATE:
                # ack the creation request
                connection.sendall ("OK".encode ())

                # get user ID from the client
                uID = connection.recv (1024).decode ()
                
                # check if this user ID has already been registered
                with open ('users.json') as f:
                    data = json.load (f)

                    for credential in data:
                        if credential["id"] == uID:
                            error_msg = COLORS.red + "This username has already been registered. If this is you, try logging in." + COLORS.clear
                            connection.send (error_msg.encode ())
                            os._exit (1)
                
                # if not, then send an OK
                connection.sendall ("OK".encode ())

                # next, get the record (v, N)
                v = connection.recv (2048).decode ()
                connection.sendall (v.encode ())

                N = connection.recv (2048).decode ()
                connection.sendall (N.encode ())

                # ensure that we have the right values
                ack = connection.recv (1024).decode ()

                # once we have these values, write it into our JSON file
                creds = {}
                with open ('users.json') as f:
                    data = json.load (f)
                
                data.append ({
                    "id": uID,
                    "record": [v, N]
                })

                with open ('users.json', 'w+') as f:
                    json.dump (data, f, indent = 4)
                
                # confirm credential creation
                confirmation = COLORS.green + "Credentials for " + uID + " created successfully!" + COLORS.clear
                print (confirmation)
                connection.sendall (confirmation.encode ())
            
            # if user wishes to authenticate
            elif choice == SIG_AUTH:
                # ack the creation request
                connection.sendall ("OK".encode ())

                # get user ID from the client
                uID = connection.recv (1024).decode ()
                
                # check if this user ID is actually registered
                flag = False
                with open ('users.json') as f:
                    data = json.load (f)

                    for credential in data:
                        if credential["id"] == uID:
                            flag = True
                            break

                # if its a new username
                if not flag:
                    error_msg = COLORS.red + "This username is not registered. Use python client.py -create to create new credentials." + COLORS.clear
                    connection.send (error_msg.encode ())
                    os._exit (1)
                
                # if its an existing user, send OK
                connection.sendall ("OK".encode ())
            else:
                print ("What")

            try:
                # simple echo server
                while True:
                    data = connection.recv(2048).decode ()
                    connection.sendall (data.encode ())
            except:
                print (COLORS.red + "Client forcibly closed the connection" + COLORS.clear)
                connection.close ()
                os._exit(1)

