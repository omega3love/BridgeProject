import pygame
import math
from bridgeMain import *

#Description
#Convert Grid (0,0) ~ (6,6) to Relative Pixel Position about the center

def GridToPixel(col, row):
    if col>0 and col<girdSize and row>0 and row<girdSize:
        pixelY = 60*(col-4)+30
        pixelX = 60*(row-4)+30
        return (pixelX,pixelY)

#Description
#Inverse function of GridToPixel Function

def PixelToGrid(pixelX, pixelY):
    col = pixelY/60+4
    row = pixelX/60+4
    return (col,row)
    
#Description
#Check Connection of Two postions
def CheckConnection(Map, col1, row1, col2, row2):
	if Map[col1][row1]^Map[col2][row2] > 0 and Map[col1][row1] != 0 and Map[col2][row2] != 0:
		return True
	else: 
		return False

#Descripstion
#Check Victory Condition (by junu)
def CheckV(Map, col, row):
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