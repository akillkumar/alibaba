'''
    CS-1340 Computer Networks
    Monsoon 2020
    
    Course Project
    @Authors: Akhil Kumar, Dhruv Khandelwal, Dhruva Panyam

    For now this is a simple echo server 
'''


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

            # simple echo server
            while True:
                data = connection.recv(2048).decode ()
                connection.sendall (data.encode ())

