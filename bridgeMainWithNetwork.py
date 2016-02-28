#! /usr/bin/python
import pygame
from bridgeClient import bridgeConnection

def main():
    
    screenSize = (screenWidth, screenHeight)
    screen = pygame.display.set_mode(screenSize)
    clock  = pygame.time.Clock()
    fps = 30 # frames per seconds       
    
    pygame.init()
    # connect to the server
    conn = bridgeConnection()
    
    # main loop for the game display
    while True:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
		pygame.quit()

	screen.fill(WHITE)
	""" ====== OUR CODES ====== """
	# How to use 'bridgeConnection'
	# [1] (ftn)  conn.sendData(data)    
	#     Send data to the server.
	#     Basically, data is delivered to your opponent via server.
	#     ( you ) -> ( server ) -> ( opponent )
	#     Your data must be the string type.
	# [2] (list) conn.dataList
	#     All data you got is saved in this list.
	#     Especially, when the game starts, the server (not the opponent)
	#     sends you the data 'initialize'.
	# [3] (ftn)  conn.disconnect()
	#     Close the connection. If you want to make another connection
	#     to restart the game for example, then you should re-initialize
	#     the class 'bridgeConnection'
    	""" ======================= """
	pygame.display.update()
	clock.tick(fps)
  
if __name__ == "__main__":
    main()
