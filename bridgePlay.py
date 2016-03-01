from bridgeSprites import *

class Play():
    def __init__(self):
        self.turn = 1
        self.grid = [[0 for x in range (0,gridSize)] for x in range (0,gridSize)]
        
    def fillGrid(self,index):
        self.grid[index[0]-1][index[1]-1]=self.turn
        self.turn *= -1

    def displayStone(self,mouse):    
        stone = Stone(self.turn)
        stone.draw(screen,(mouse[0],mouse[1]))
    
    def throwStone(self):
        for x in range (0,gridSize):
            for y in range (0,gridSize):    
                if self.grid[x][y]==1 or self.grid[x][y]==-1:
                    relativePixel = gridToPixel((x+1,y+1))
                    absPixel = relToAbs(relativePixel)
                    stone = Stone(self.grid[x][y])
                    stone.draw(screen,absPixel)

    def isEnded():
        pass


