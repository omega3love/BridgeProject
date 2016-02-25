from twisted.internet import reactor, protocol

PORT = 50001

class MyServer(protocol.Protocol):
    pass

class MyServerFactory(protocol.Factory):
    protocol = MyServer

factory = MyServerFactory()
reactor.listenTCP(PORT, factory)
reactor.run()
