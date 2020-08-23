#!/usr/bin/env python2

################################################################################################################
# Name      : Sagar Surendran
# UTA ID    : 1001348700
# Date      : 08/09/2020
# Brief     : Server implementaion of multi threaded 
#             server client with Message Broker program with simple GUI
#
# The multi threaded server program has been inspired from the server.py from the below source
# https://levelup.gitconnected.com/learn-python-by-building-a-multi-user-group-chat-gui-application-af3fa1017689
# https://raw.githubusercontent.com/effiongcharles/multi_user_chat_application_in_python/master/server_gui.py
################################################################################################################

import Tkinter as tk
import socket
import threading
import csv
import time 
import json

window = tk.Tk()
window.title("Sever")

# Top frame consisting of two buttons widgets (i.e. btnStart, btnStop)
topFrame = tk.Frame(window)
btnStart = tk.Button(topFrame, text="Connect", command=lambda : start_server())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(topFrame, text="Stop", command=lambda : stop_server(), state=tk.DISABLED)
btnStop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(5, 0))

# Middle frame consisting of two labels for displaying the host and port info
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text = "Host: X.X.X.X")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text = "Port:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

# The client frame shows the client area
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="**********Client List**********").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=15, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))


server = None
HOST_ADDR = "0.0.0.0"
HOST_PORT = 8080
client_name = " "
clients = []
clients_names = []

qA = []
qB = []
qC = []

l1=[]
l2=[]
l3=[]


u1 = ["Meter", "Millimeter", "Centimeter", "Kilometer", "Astronomical Unit"]
u2 = ["Parsec", "Light Year", "Inch", "Foot", "Yard"]
u3 = ["Horse", "Nautical Mile", "American football field", "Hand", "Mile"]

#Reading the conversion rules from the stored file.
with open("conversion_rule.txt") as f:
    reader = csv.reader(f)
    ll = list(reader)

l1 = ll[0]
l2 = ll[1]
l3 = ll[2]

# Start server function
def start_server():
    global server, HOST_ADDR, HOST_PORT # code is fine without this
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print socket.AF_INET
    print socket.SOCK_STREAM

    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)  # server is listening for client connection

    threading._start_new_thread(accept_clients, (server, " "))

    lblHost["text"] = "Host: " + HOST_ADDR
    lblPort["text"] = "Port: " + str(HOST_PORT)


# Stop server function
def stop_server():
    global server
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)


def accept_clients(the_server, y):
    while True:
        client, addr = the_server.accept()
        clients.append(client)

        # use a thread so as not to clog the gui thread
        threading._start_new_thread(send_receive_client_message, (client, addr))


# Function to receive message from current client AND
# Send that message to other clients
def send_receive_client_message(client_connection, client_ip_addr):
    global server, client_name, clients, clients_addr
    client_msg = " "

    # send welcome message to client
    client_name  = client_connection.recv(4096)
    client_connection.send("Welcome " + client_name + ". \n You have two options. \n 1. To upload a message, type a decimal value, and type the queue name and press send.\n 2. Type queue name and press Retrieve to retrieve the queue.\n Type 'exit' to quit")

    clients_names.append(client_name)

    update_client_names_display(clients_names)  # update client names display


    while True:
        data = client_connection.recv(4096)
        if not data: break
        if data == "exit": break

        client_msg = data

        if '-' in client_msg:
            mssg = client_msg
            val, que = mssg.replace("'","").split("-")
            if que == "A":
                qA.append(val)
                with open('q1.txt', 'w') as ile1:
                    json.dump(qA, ile1)
            elif que == "B":
                qB.append(val)
                with open('q2.txt', 'w') as ile2:
                    json.dump(qB, ile2)
            elif que == "C":
                qC.append(val)
                with open('q3.txt', 'w') as ile3:
                    json.dump(qC, ile3)
        else:
            que = client_msg
            if que == "A":
                with open("q1.txt", 'r') as f1:
                    try:
                        quA = json.load(f1)
                    except:
                        quA = []
                Q = quA
                lis = l1
                unit = u1
            elif que == "B":
                with open("q2.txt", 'r') as f2:
                    try:
                        quB = json.load(f2)
                    except:
                        quB = []
                Q = quB
                lis = l2
                unit = u2
            elif que == "C":
                with open("q3.txt", 'r') as f3:
                    try:
                        quC = json.load(f3)
                    except:
                        quC = []
                Q = quC
                lis = l3
                unit = u3

            if not Q:
                client_connection.send(que +" is empty")
            else:
                for content in Q:
                    mul_list = [float(elem) * float(content) for elem in lis ]
                    for val1, val2 in zip(mul_list,unit):
                        val = str(val1) + " " + val2
                        client_connection.send(val)
                        time.sleep(1)
                if que == "A":
                    f = open('q1.txt', 'w')
                    f.close()
                if que == "B":
                    f = open('q2.txt', 'w')
                    f.close()
                if que == "C":
                    f = open('q3.txt', 'w')
                    f.close()

    # find the client index then remove from both lists(client name list and connection list)
    idx = get_client_index(clients, client_connection)
    del clients_names[idx]
    del clients[idx]
    client_connection.send("BYE!")
    client_connection.close()

    update_client_names_display(clients_names)  # update client names display


# Return the index of the current client in the list of clients
def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


# Update client name display when a new client connects OR
# When a connected client disconnects
def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c+"\n")
    tkDisplay.config(state=tk.DISABLED)


window.mainloop()
