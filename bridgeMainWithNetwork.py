#! /usr/bin/python
from bridgePlay import *
from bridgeClient import *

def main():
    
    pygame.init()
    # connect to the server
    conn = bridgeConnection()
    board = Board()
    play = Play()

    # main loop for the game display
    while True:
        mouse = pygame.mouse.get_pos()
	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
		pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:   

                pixel=absToRel(mouse)                                      
                index=pixelToGrid(pixel)
                indexString = tupleToStr(index)

                if 'initialize' in conn.dataList['cmd']:
                    # Send the Data only when the grid is empty(==0)
                    if indexString not in conn.dataList['grid']:
                       conn.sendData(indexString)
                       print ("Data sent was successful!")
                    else:
                       pass
                    # Need to message to player when grid is already filled
                    #
                    #
                    #
                    #
                    ########################################################

        play.turn = 1            
        for gridString in conn.dataList['grid']:
            #print ("Something is going on")
            grid=strToTuple(gridString)
            play.fillGrid(grid)
        
        
	screen.fill(WHITE)
        board.draw(screen)
        play.displayStone(mouse)
        play.throwStone()

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
