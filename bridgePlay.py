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
                    
# Check Connection bwt Two points
    def isConnected(self,grid,colx,rowx,coly,rowy):
	if grid[colx][rowx]^Map[coly][rowy] > 0 and grid[colx][rowx] != 0 and grid[coly][rowy] != 0:
		return True
	else:
		return False

# Check Game over by connecting bridge
    def isEnded_C(self,grid,col,row):
	lenmap = len(grid)
	for Checker in range(lenmap):
		if Checker == lenmap - 1:
			return True
		elif not isConnected(grid,Checker,row-1,Checker+1,row-1):
			break
	for Checker in range(lenmap):
		if Checker == lenmap - 1:
			return True
		elif not isConnected(grid,col-1,Checker,col-1,Checker+1):
			break
	for Checker in range(lenmap-abs(col-row)):
		if lenmap-abs(col-row) > 1:
			if Checker == lenmap-abs(col-row)-1:
				return True
			elif col < row:
				if not isConnected(grid,Checker,row-col+Checker,Checker+1,row-col+Checker+1):
					break
			elif col >= row:
				if not isConnected(grid,col-row+Checker,Checker,col-row+Checker+1,Checker+1):
					break
	for Checker in range(lenmap-abs(lenmap+1-col-row)):
		if 2 < col+row < lenmap*2:
			if Checker == lenmap-abs(lenmap+1-col-row)-1:
				return True
			elif col > lenmap+1-row:
				if not isConnected(grid,col+row-lenmap-1+Checker,lenmap-1-Checker,col+row-lenmap+Checker,lenmap-1-Checker-1):
					break
			elif col <= lenmap+1-row:
				if not isConnected(grid,Checker,col+row-2-Checker,Checker+1,col+row-2-Checker-1):
					break
	return False


