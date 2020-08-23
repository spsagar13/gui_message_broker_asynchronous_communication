#!/usr/bin/env python2
#############################################################################
# Name      : Sagar Surendran
# UTA ID    : 1001448700
# Date      : 08-09-2020
# Brief     : Client implementation of the multi threaded
#             server client program
#
# The client program has been inspired from the below chat app implementaion
# https://levelup.gitconnected.com/learn-python-by-building-a-multi-user-group-chat-gui-application-af3fa1017689
# https://raw.githubusercontent.com/effiongcharles/multi_user_chat_application_in_python/master/client_gui.py
#############################################################################

import Tkinter as tk
import tkMessageBox 
import socket
import threading

window = tk.Tk()
window.title("Client")
username = " "


# Implementation of all the buttons
topFrame = tk.Frame(window)
lblName = tk.Label(topFrame, text = "Name:").pack(side=tk.LEFT)
entName = tk.Entry(topFrame)
entName.pack(side=tk.LEFT)
btnConnect = tk.Button(topFrame, text="Connect", command=lambda : connect())
btnConnect.pack(side=tk.RIGHT)
topFrame.pack(side=tk.TOP)

topFrame2 = tk.Frame(window)
lblName2 = tk.Label(topFrame2, text = "Decimal value in meters and Queue name seperated by hyphen (eg: 10-A):").pack(side=tk.LEFT)
entName2 = tk.Entry(topFrame2)
entName2.pack(side=tk.LEFT)
btnConnect2 = tk.Button(topFrame2, text="Upload", command=lambda : send_msg(entName2, 2))
btnConnect2.pack(side=tk.RIGHT)
topFrame2.pack(side=tk.TOP)

topFrame4 = tk.Frame(window)
lblName4 = tk.Label(topFrame4, text = "Queue Name (A, B or C):").pack(side=tk.LEFT)
entName4 = tk.Entry(topFrame4)
entName4.pack(side=tk.LEFT)
btnConnect4 = tk.Button(topFrame4, text="Retrieve", command=lambda : send_msg(entName4, 4))
btnConnect4.pack(side=tk.RIGHT)
topFrame4.pack(side=tk.TOP)

displayFrame = tk.Frame(window)
scrollBar = tk.Scrollbar(displayFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(displayFrame, height=20, width=55)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
tkDisplay.tag_config("tag_our_message", foreground="blue")
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
displayFrame.pack(side=tk.TOP)

bottomFrame = tk.Frame(window)
tkMessage = tk.Text(bottomFrame, height=2, width=55)
tkMessage.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
tkMessage.config(highlightbackground="grey", state="disabled")
tkMessage.bind("<Return>", (lambda event: getChatMessage(tkMessage.get("1.0", tk.END))))
bottomFrame.pack(side=tk.BOTTOM)


def connect():
    global username, client
    if len(entName.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
    else:
        username = entName.get()
        connect_to_server(username)


# network client
client = None
HOST_ADDR = "0.0.0.0"
HOST_PORT = 8080

def connect_to_server(name):
    global client, HOST_PORT, HOST_ADDR
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST_ADDR, HOST_PORT))
        client.send(name) # Send name to server after connecting

        entName.config(state=tk.DISABLED)
        btnConnect.config(state=tk.DISABLED)
        tkMessage.config(state=tk.NORMAL)

        # start a thread to keep receiving message from server
        # do not block the main thread :)
        threading._start_new_thread(receive_message_from_server, (client, "m"))
    except Exception as e:
        tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + HOST_ADDR + " on port: " + str(HOST_PORT) + " Server may be Unavailable. Try again later")


def receive_message_from_server(sck, m):
    while True:
        from_server = sck.recv(4096)

        if not from_server: break

        # display message from server on the chat window

        # enable the display area and insert the text and then disable.
        texts = tkDisplay.get("1.0", tk.END).strip()
        tkDisplay.config(state=tk.NORMAL)
        if len(texts) < 1:
            tkDisplay.insert(tk.END, from_server)
        else:
            tkDisplay.insert(tk.END, "\n\n"+ from_server)

        tkDisplay.config(state=tk.DISABLED)
        tkDisplay.see(tk.END)


    sck.close()
    window.destroy()


def getChatMessage(msg):

    msg = msg.replace('\n', '')
    texts = tkDisplay.get("1.0", tk.END).strip()

    # enable the display area and insert the text and then disable.
    # why? Apparently, tkinter does not allow use insert into a disabled Text widget :(
    tkDisplay.config(state=tk.NORMAL)
    if len(texts) < 1:
        tkDisplay.insert(tk.END, "You->" + msg, "tag_your_message") # no line
    else:
        tkDisplay.insert(tk.END, "\n\n" + "You->" + msg, "tag_your_message")

    tkDisplay.config(state=tk.DISABLED)

    send_mssage_to_server(msg)

    tkDisplay.see(tk.END)
    tkMessage.delete('1.0', tk.END)


def send_msg(entName, option):
    msg = entName.get()
    
    op="u"
    if option == 4:
        op="d"

    texts = tkDisplay.get("1.0", tk.END).strip()
    tkDisplay.config(state=tk.NORMAL)

    if op == "u":
        mssg = msg
        a, b = mssg.replace("'","").split("-")
        tkDisplay.insert(tk.END, "\n\n" + "Uploading " + a + " to queue " + b, "tag_your_message")
    else:
        tkDisplay.insert(tk.END, "\n\n" + "Downloading values from Queue " + msg, "tag_your_message")

    client.send(msg)
    tkDisplay.see(tk.END)
    tkMessage.delete('1.0', tk.END)

def send_mssage_to_server(msg):
    client.send(msg)
    if msg == "exit":
        client.close()
        window.destroy()
    print("Sending message")


window.mainloop()

