'''
    CS-1340 Computer Networks
    Monsoon 2020
    
    Course Project
    @Authors: Akhil Kumar, Dhruv Khandelwal, Dhruva Panyam

    For now this is a simple echo server 
'''

import os
import socket

from helper import *

# create client socket
with socket.socket (socket.AF_INET, socket.SOCK_STREAM) as client:
    
    # connect to the server
    try:
        client.connect (server_addr)
        print (COLORS.green + "Connected to server" + COLORS.clear)
    except:
        print (COLORS.red + "Could not establish connection to server" + COLORS.clear)
        os._exit(1)

    while True:
        client.sendall (input().encode())

        data = client.recv (2048).decode()

        print ("Server said:", data)

