#! /usr/bin/python
from bridgePlay import *
from bridgeClient import *

def main():
    
    pygame.init()
    # connect to the server
    conn = bridgeConnection()
    board = Board()
    play = Play()
    turn = 1


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
		    if indexString not in conn.dataList['grid'] and indexString != '6':
                       conn.sendData(indexString)
                    else:
                       pass
                    # Need to message to player when grid is already filled
                    #
                    #
                    #
                    #
                    ########################################################

        if 'pickNumber' in conn.dataList['cmd'] and 'pickIsDone' not in conn.dataList['cmd']:
           number = input('Pick Any Number: ')
           conn.sendData(str(number)+'PN')  ## Make Length three
           while len(conn.dataList['turn'])<2:
              pass
           conn.sendData('pickIsDone')    




        for gridString in conn.dataList['grid']:
            play.turn = -((conn.dataList['grid'].index(gridString))%2*2-1)
            grid = strToTuple(gridString)
            play.fillGrid(grid)
            if play.isEnded_C(grid[0],grid[1])==True:
                    print play.isEnded_C
                    pygame.quit()
        

	screen.fill(WHITE)
        board.draw(screen)
        play.turn = turn
        play.throwStone()
        play.displayStone(mouse)

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
