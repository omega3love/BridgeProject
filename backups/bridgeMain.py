#! /usr/bin/python
from bridgePlay import *


def main():
 
    """ Initialize pygame and set parameters """
    pygame.init()
    board = Board()
    play = Play()

    """ Display Loop """
    while True:
        mouse = pygame.mouse.get_pos()

	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
		pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                pixel=absToRel(mouse)
                index=pixelToGrid(pixel)
                play.fillGrid(index)

	print pixel
	print index
#	if play.isEnded_C():
#	    pygame.quit()
	
	
	
	screen.fill(WHITE)
        board.draw(screen)

        play.displayStone(mouse)
        play.throwStone()

	pygame.display.update()
	clock.tick(fps)
  
if __name__ == "__main__":
    main()
