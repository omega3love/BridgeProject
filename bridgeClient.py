#! /usr/bin/python

import socket
import threading
from time import sleep

class bridgeConnection():
    
    def __init__(self):
		
	self.HOST = raw_input("HOST IP : ")
	self.PORT = 50000
	self.DATA_SIZE = 128 # maximum data length which can be sent in once
	
	self.soc = self.makeConnection()
	self.dataList = []
	# Threading allows to get data whenever it's delievered
	T = threading.Thread(target = self.receiveData)
	T.start()
	
	""" for test """
	while 1:
	    msg = raw_input("send data : ")
	    if msg == "quit" or "exit":
		break
	    self.sendData(msg)

    def makeConnection(self):
	
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	soc.settimeout(10.0) # maximum wating time (seconds)
	    
	connected = False
	while not connected:
	    try:
		print 'trying to connect ' + self.HOST
		soc.connect( (self.HOST, self.PORT) )
		connected = True
		print 'Connected!'
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
	else:
	    print "Data packet size exceeded!"
	
    def receiveData(self):
	""" Receive data (string type) from the server """
	while True:
	    try:
		data = self.soc.recv(DATA_SIZE) # receive data whose length <= DATA_SIZE
	    except:
		print "Connection is lost"
		break
	    if data:
		self.dataList.append( data ) # save the received data
	self.soc.close() # disconnect the connection
    
if __name__ == "__main__":
    client = bridgeConnection()
    