#! /usr/bin/python

import socket
import threading
from time import sleep
import sys

class bridgeConnection():
    
    def __init__(self):
		
	#self.HOST = raw_input("HOST IP : ")
	self.HOST = "143.248.2.116"
	self.PORT = 50000
	self.DATA_SIZE = 128 # maximum data length which can be sent in once
	
	self.endThread = False
	self.soc = self.makeConnection()
	self.dataList = []
	# Threading allows to get data whenever it's delievered
	#T = threading.Thread(target = self.receiveData)
	#T.start() 
	
	""" for test """
	if not self.soc:
	    print "Server not opened"
	else:
	    T = threading.Thread(target = self.receiveData)
	    T.start() 
	    while 1:
		msg = raw_input("send data : ")
		self.sendData(msg)
		if msg == "quit" or msg == "exit":
		    self.endThread = True
		    break
	
	print "joining the thread..."
	T.join()
	print "thread is joined"
	sys.exit()
	
    def makeConnection(self):
	
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	soc.settimeout(6.0) # maximum wating time (seconds)
	    
	connected = False
	while not connected:
	    try:
		print 'trying to connect ' + self.HOST
		soc.connect( (self.HOST, self.PORT) )
		connected = True
		print 'Connected!'
		#soc.settimeout(None)
		break
	    
	    except socket.timeout:
		print 'Exceeded time limit'
		break
	    
	    except socket.error:
		print 'Access denied'
		sleep(1)
		# [ NOT YET ] if QUIT command is received, call 'sys.exit'
		return False
		
	return soc

    def sendData(self, data):
	""" Send data (string type) to the server """
	if len(data) <= self.DATA_SIZE:
	    self.soc.send(data.encode('UTF-8'))
	    print "Data '%s' is sent successfully" %data
	else:
	    print "Data packet size exceeded!"
	
    def receiveData(self):
	""" Receive data (string type) from the server """
	while not self.endThread:
	    sleep(0.5)
	    try:
		data = self.soc.recv(self.DATA_SIZE) # receive data whose length <= DATA_SIZE
		print "data is : %s" %data
	    except socket.timeout:
		print "socket timed out"
		continue
	    except:
		print "Connection is lost"
		break
	    
	    if data:
		self.dataList.append( data ) # save the received data
	self.soc.close() # disconnect the connection
    
if __name__ == "__main__":
    client = bridgeConnection()
    