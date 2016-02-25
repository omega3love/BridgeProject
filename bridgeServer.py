#! /usr/bin/python

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from time import sleep

myhost = '127.0.0.1'

class Server(Protocol):

    def connectionMade(self):
	
        # self.transport.write("""connected""")
        self.factory.clients.append(self)
        self.peer = self.transport.getPeer()
        print vars(self.peer) # show who made the connection
        
        if self.peer.host == myhost:
            self.factory.host = self
        
        """ Initialize the game when enough players are connected """
        if len(self.factory.clients) == 2:
	    sleep(2.5) # wait before starting the game
            self.message_all('initialize') # when clients receive this msg, they starts the game
            
    def connectionLost(self, reason):
	""" When a client lose a connection """
        print "connection lost ", self
        self.factory.clients.remove(self)

    def dataReceived(self, data):
	""" If data is delivered from a client to the server,
	    deliver the data to other clients """
        sender = self.transport.getPeer().host # address of data sender
        
        for clients in self.factory.clients:
            if not clients.peer.host == sender:
                clients.transport.write(data)

    def message_all(self, msg):
	""" Send message to all clients from server """
        for clients in self.factory.clients:
            clients.transport.write(msg)

    def message_to(self, clients_num, msg):
	""" Send message to a certain client from server """
        if clients_num in range(1, len(self.factory.clients) + 1):
            self.factory.clients[clients_num].transport.write(msg + '\n')

factory = Factory()
factory.protocol = Server
factory.clients = [] # clients list
factory.host = None

PORT = 50000 # port of the server
reactor.listenTCP(PORT, factory)
reactor.run()

