#! /usr/bin/python   
import time                                           
from bridgePlay import *                                        
from bridgeClient import *                                      

def main():

    pygame.init()

    conn = bridgeConnection(screen)
    board = Board()

#####################################################################

    """ Turn Attribution """

    ''' Picking Process '''
    
    while 'pickNumber' not in conn.dataList['cmd']:
        print ("Catch your opponent \n")
        time.sleep(60)
        
    
    if 'pickNumber' in conn.dataList['cmd'] and 'initialize' not in conn.dataList['cmd']:

        if 'A' in  conn.dataList['ask']:
            while number != 1 or number != 2:
                number = input("Pick number 1 or 2 \n")
            conn.sendData("pick:A:%d" %number)    
        elif 'B' in conn.dataList['ask']:
            while 0 < number < 101:
                number = input("Pick Any integer from 1 to 100: ")
            conn.sendData("pick:B:%d" %number)

    while len(conn.dataList['pick'])<2:
        print ("Your oppoent is betting. Please Wait \n")
        time.sleep(5)
    
    ''' Number attribution '''    

    for pickData in conn.dataList['pick']:
        if 'A' in pickData:
            askingUserNum = int(pickData[-1])
        if 'B' in pickData:
            askedUserNum = int(pickData[-1])
    
    ''' Betting Process '''

    if (askingUserNum+askedUserNum)%2==1:
        if 'A' in conn.dataList['ask']:
            turn = 1
        elif 'B' in conn.dataList['ask']:
            turn = -1
    elif (askingUserNum+askedUserNum)%2==0:
        if 'A' in conn.dataList['ask']:
            turn = -1
        elif 'B' in conn.dataList['ask']:
            turn = 1
            
    conn.sendData("cmd:initialize")         
        
######################################################################
   
    play = Play(turn)  
  
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    ___Play Class___

    Play object represents have two member variables
  
    Member Variables:
    1. turn : 1 for his turn, -1 for enemy
    2. grid : 6*6 array which contatins the stone position information

    Member Functions:
    1. fillGrid(index) : fill self.grid with an index (tuple) 
    2. drawStone() : Draw all stones in self.grid on the borad
    3. isEnded_C(col, row) : ??? Made by Junu
    4. isConnected(??) : ??? Made by Junu

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
       
    game_End = (False, False)    
    event_ButtonUp = False

    
    while True:

        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                pixel=absToRel(mouse)                       
                index=pixelToGrid(pixel)
                indexString = tupleToStr(index)

                if play.turn==1:
                    if indexString not in conn.dataList['grid'] and indexString != '6':
                        conn.sendData("grid:%s" %indexString)
                    else:
                        print("That position is already occupied! \n")


        for gridString in conn.dataList['grid']:
            grid = strToTuple(gridString)
            play.fillGrid(grid)


        screen.fill(WHITE)
        board.draw(screen)
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
                                               














