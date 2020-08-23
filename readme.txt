# Name   : Sagar Surendran
# UTA ID : 1001438700
# Brief  : Readme file for multi threaded server client program with Message broker in GUI

#####################################################################################################################
# https://levelup.gitconnected.com/learn-python-by-building-a-multi-user-group-chat-gui-application-af3fa1017689
# https://raw.githubusercontent.com/effiongcharles/multi_user_chat_application_in_python/master/server_gui.py
# https://levelup.gitconnected.com/learn-python-by-building-a-multi-user-group-chat-gui-application-af3fa1017689
# https://raw.githubusercontent.com/effiongcharles/multi_user_chat_application_in_python/master/client_gui.py
#####################################################################################################################

Prerequisites
-------------
	Linux based machine/MacOS
	Python 2.x

	Below packages
	  tkMessageBox
	  socket
	  threading
	  Tkinter
	  time
	  csv
	  json

Sanity checks
-------------
   After unzipping it, you will see the below files.
   1. server.py  - md5 34f2bf3cc12b014f4c77f984a958850f
   2. client.py  - md5 8b87be00af582068aec85b8c03649754 
   3. conversion_rule.txt
   4. q1.txt
   5. q2.txt
   6. q3.txt
   7. readme.txt    

Execution steps: 
---------------
 chmod 777 server.py
 chmod 777 client.py

Steps:
......
4 Terminals should be opened, for Server and 3 Clients

In terminal 1
  1. Type ./server.py # GUI for the server will be opened
  2. click on the "Start Server" button
In terminal 2
  3. Type ./client.py # GUI for the client 1 will be opened
  4. Type a required name and press enter
In terminal 3
  5. Type ./client.py # GUI for the client 2 will be opened
  6. Type a required name and press enter
In terminal 4
  7. Type ./client.py # GUI for the client 3 will be opened
  8. Type a required name and press enter


To upload a message, decimal value in meters along with the queue name shall be given to upload. 
Eg: if we want to upload the decimal 10 to queue A, one should type 10-A

Upon clicking the retrieve, after typing from which queue it shall be retrieved, the data shall be retrieved
................................................................................................
-> To verify the duplicate name check, the same name can be given when creating the client name
ASSUMPTION : upper case/lower case versions of the same name is considerd equivalent 
-> To stop the counter, in any Client GUI, "Stop counter" button can be pressed.
   If the counter is running, it will stop the counter. If the counter is not running, it will
   display the appropriate message
-> To exit the client, either close the GUI window, or type "{quit}" and press enter
-> To exit server, either close the GUI or press "Stop Server" button
................................................................................................

