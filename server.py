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
import random 
from hashlib import sha256
import threading

from helper import *

random_facts = {
    'animals':[
        "Dogs are animals",
        "Cats are animals",
        "A lion has four legs",
        "Bees have 5 eyes"
    ],
    'history':[
        "JFK is dead",
        "Humans were smart"
    ]
}

def get_search_matches(keyword):
    res = []
    keyword = keyword.lower()
    for key in random_facts:
        if key.lower().__contains__(keyword) and len(keyword) > len(key)/2:
            res = res + random_facts[key]
            continue

        for fact in random_facts[key]:
            if fact.lower().__contains__(keyword):
                res.append(fact)
    
    return res


def create_credentials(connection, client_addr):
    # get user ID from the client
    uID = connection.recv (1024).decode ()

    # check if this user ID has already been registered
    with open ('users.json') as f:
        data = json.load (f)

        for credential in data:
            if credential["id"] == sha256(uID.encode()).hexdigest():
                error_msg = COLORS.red + "This username has already been registered. If this is you, try logging in." + COLORS.clear
                connection.send (error_msg.encode ())
                return
                # os._exit (1)

    # if not, then send an OK
    connection.sendall ("OK".encode ())

    # next, get the record (v, N)
    v = connection.recv (2048).decode ()
    connection.sendall (v.encode ())

    N = connection.recv (2048).decode ()
    connection.sendall (N.encode ())

    # ensure that we have the right values
    ack = connection.recv (1024).decode ()
    print('ack:',ack)
    if not ack == "OK":
        print(COLORS.red + "An error was detected in the credentials. Please try again." + COLORS.clear)
        # connection.close()
        return

    # once we have these values, write it into our JSON file

    with open ('users.json') as f:
        data = json.load (f)

    data.append ({
        "id": sha256(uID.encode()).hexdigest(),
        "record": [v, N]
    })

    with open ('users.json', 'w+') as f:
        json.dump (data, f, indent = 4)

    # confirm credential creation
    confirmation = COLORS.green + "Credentials for " + uID + " created successfully!" + COLORS.clear
    print (confirmation)
    connection.sendall (confirmation.encode ())
    return


def validate_credentials(connection, client_addr):
    # get user ID from the client
    uID = connection.recv (1024).decode ()
    
    # check if this user ID is actually registered
    flag = False
    record = []
    with open ('users.json') as f:
        data = json.load (f)

        for credential in data:
            if credential["id"] == sha256(uID.encode()).hexdigest():
                flag = True
                record = credential["record"]
                break

    # if its a new username
    if not flag:
        error_msg = COLORS.red + "This username is not registered. Use python client.py -create to create new credentials." + COLORS.clear
        connection.send (error_msg.encode ())
        return
    
    # if its an existing user, send OK
    connection.sendall ("OK".encode ())

    # now, client sends y
    y = (connection.recv (4096).decode ())
    y = json.loads(y)
    
    # calculate a random bit-string b = {0, 1}^NUM_TRIALS
    b = ''.join([str(random.randrange(0,2)) for _ in range(NUM_TRIALS)])

    # send b to client
    connection.sendall (str(b).encode ())

    # client sends z
    z = (connection.recv (6144).decode ())
    z = json.loads(z)   # array of z's

    # validate the user
    v = int (record[0])
    N = int (record[1])

    flag = 0
    for i in range(NUM_TRIALS):
        if y[i] == 0 or modexp (z[i], 2, N) != (y[i] * (v ** int(b[i]))) % N:
            flag = 1
            break
    
    if flag:
        confirmation = COLORS.red + "Access denied!" + COLORS.clear
    else:
        confirmation = COLORS.green + "Access granted!" + COLORS.clear

    # send confirmation
    print (confirmation + " - " + uID)
    conf_data = {'success': not flag, 'message':confirmation}
    connection.sendall (json.dumps(conf_data).encode ())  

    if flag:
        return

    try:
        search_keyword = connection.recv(1024).decode()
        data = get_search_matches(search_keyword)
        connection.sendall (json.dumps(data).encode())
    except:
        return

    return


def handle_client(connection, client_addr):
    if connection:
        try:
            print (COLORS.green + "Connected to client", client_addr, COLORS.clear)

            # TODO: fork () here to handle multiple clients
            # I'm not doing it since I'm on Windows and fork () is a BT

            # first message from client will be either a 1 or a 0 to indicate the activity
            # 0 - user credential creation
            # 1 - user authentication
            choice = connection.recv (1024).decode ()

            if choice == SIG_CREATE:

                # ack the creation request
                connection.sendall ("OK".encode ())
                create_credentials(connection, client_addr)
                print (COLORS.yell + "Disconnected from", client_addr, COLORS.clear)
                connection.close()
                return
            
            # if user wishes to authenticate
            elif choice == SIG_AUTH:
                # ack the creation request
                connection.sendall ("OK".encode ())

                validate_credentials(connection, client_addr)
                print (COLORS.yell + "Disconnected from", client_addr, COLORS.clear)
                connection.close()
                return

                             
            else:
                print ("What")
        except:
            print (COLORS.red + "Client forcibly closed the connection" + COLORS.clear)
            print (COLORS.yell + "Disconnected from", client_addr, COLORS.clear)
            connection.close ()
            # os._exit(1)




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

        threading._start_new_thread(handle_client, (connection, client_addr,))

        # if we have a valid connection
        