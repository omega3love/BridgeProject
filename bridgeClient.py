#! /usr/bin/python

import socket
from time import sleep

HOST = raw_input("HOST IP : ")
PORT = 50000
DATA_SIZE = 128 # maximum data length which can be sent in once

def makeConnection(host, port):
    
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.settimeout(10.0) # maximum wating time (seconds)
        
    connected = False
    while not connected:
	try:
	    print 'trying to connect ' + host
	    soc.connect( (host, port) )
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
	    
if __name__ == "__main__":
    makeConnection(HOST, PORT)