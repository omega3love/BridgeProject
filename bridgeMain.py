#! /usr/bin/python

"""

"""

import pygame
from bridgeSprites import *

def main():
  
    """ Initialize pygame and set parameters """
    pygame.init()
    
    screenSize = (800,800)
    screen = pygame.display.set_mode(screenSize)
    clock  = pygame.time.Clock()
    fps = 30 # frames per seconds
    
    """ Declare sprites """

    
    
    """ Display Loop """
    while True:
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
		pygame.quit()
	
	screen.fill(WHITE)
	
	pygame.display.update()
	clock.tick(fps)
  
if __name__ == "__main__":
    main()