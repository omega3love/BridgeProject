from bridgeParameters import *

#Description
#Convert Grid (1,1) ~ (6,6) to Relative Pixel Position about the center
#Grid style 
#(1,1) (1,2) (1,3) (1,4) (1,5) (1,6)
#(2,1) (2,2) (2,3) (2,4) (2,5) (2,6)
#(3,1) (3,2) (3,3) (3,4) (3,5) (3,6)
#... and so on to (6,6)

def gridToPixel(index):
    if 0 < index[0] <= gridSize and 0 < index[1] <= gridSize:
        pixelY = 60*(index[0]-4)+30
        pixelX = 60*(index[1]-4)+30
        return (pixelX,pixelY)

#Description
#Inverse function of GridToPixel Function

def pixelToGrid(pixel):
    col = pixel[1]/60+4
    row = pixel[0]/60+4
    return (col,row)

#Description
#Move the absolute position to the relatvie position to center

def absToRel(pixel):
    pixelX = pixel[0]-screenWidth/2
    pixelY = pixel[1]-screenHeight/2
    return (pixelX, pixelY)
    
def relToAbs(pixel):
    pixelX = pixel[0]+screenWidth/2
    pixelY = pixel[1]+screenHeight/2
    return (pixelX, pixelY)

#Description
#Check Connection of Two postions
def CheckConnection(Map, col1, row1, col2, row2):
	if Map[col1][row1]^Map[col2][row2] > 0 and Map[col1][row1] != 0 and Map[col2][row2] != 0:
		return True
	else: 
		return False

#Descripstion
#Check Victory Condition (by junu)
def CheckVictory(Map, col, row):
	for Checker in range(6):
		if Checker == 5:
			return True
		elif not CheckConnection(Map,Checker,col-1,Checker+1,row-1):
			break
	for Checker in range(6):
		if Checker == 5:
			return True
		elif not CheckConnection(Map,col-1,Checker,row-1,Checker+1):
			break
	if abs(col - row) < 5:
		for Checker in range(6 - abs(col - row)):
			if Checker == 6 - abs(col - row) - 1:
				return True
			elif row > col:
				if not CheckConnection(Map,Checker,col-row+Checker,Checker+1,col-row+Checker+1):
					break
			elif row <= col:
				if not CheckConnection(Map,col-row+Checker,Checker,col-row+Checker+1,Checker+1):
					break
	if abs(7 - col - row) < 5:
		for Checker in range(6 - abs(7 - col - row)):
			if Checker == 6 - abs(7 - col - row) - 1:
					return True
			elif col > 7 - row:
				if not CheckConnection(Map,col+row-7+Checker,5-Checker,col+row-7+Checker+1,5-Checker-1):
					break
			elif col <= 7 - row:
				if not CheckConnection(Map,Checker,col+row-2-Checker,Checker+1,col+row-2-Checker-1):
					break
	return False
