#! /usr/bin/python

"""

"""

import pygame
from colors import *
from bridgeSprites import *
from bridgeFunction import *

screenWidth = 600;
screenHeight = 600;
gridSize =6;

def main():
    screenSize = (screenWidth,screenHeight)
    screen = pygame.display.set_mode(screenSize)
    clock  = pygame.time.Clock()
    fps = 30 # frames per seconds       
    
    """ Initialize pygame and set parameters """
    pygame.init()
  
    board = Board()

    """ Display Loop """
    while True:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
		pygame.quit()

	screen.fill(WHITE)
        board.draw(screen)
    	
	pygame.display.update()
	clock.tick(fps)
  
if __name__ == "__main__":
    main()
