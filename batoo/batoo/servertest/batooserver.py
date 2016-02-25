from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from time import sleep

myhost = '127.0.0.1'

class Server(Protocol):

    def connectionMade(self):
        # self.transport.write("""connected""")
        self.factory.clients.append(self)
        self.peer = self.transport.getPeer()
        print vars(self.peer)
        if self.peer.host == myhost:
            self.factory.host = self
        if len(self.factory.clients) == 2:
	    sleep(2.5)
            self.message_all('initialize')

    def connectionLost(self, reason):
        print "connection lost ", self
        self.factory.clients.remove(self)

    def dataReceived(self, data):
        sender = self.transport.getPeer().host
        for clients in self.factory.clients:
            if not clients.peer.host == sender:
                clients.transport.write(data)

    def message_all(self, msg):
        for clients in self.factory.clients:
            clients.transport.write(msg)

    def message_to(self, clients_num, msg):
        if clients_num in range(1, len(self.factory.clients) + 1):
            self.factory.clients[clients_num].transport.write(msg + '\n')

factory = Factory()
factory.protocol = Server
factory.clients = []
factory.host = None

PORT = 50000
reactor.listenTCP(PORT, factory)
reactor.run()
