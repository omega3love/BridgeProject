#! /usr/bin/python
from random import randint

"""
(0,0) (0,1) (0,2) (0,3) (0,4) (0,5)
(1,0) (1,1) (1,2) (1,3) (1,4) (1,5)
(2,0) (2,1) (2,2) (2,3) (2,4) (2,5)
(3,0) (3,1) (3,2) (3,3) (3,4) (3,5)
(4,0) (4,1) (4,2) (4,3) (4,4) (4,5)
(5,0) (5,1) (5,2) (5,3) (5,4) (5,5)
"""

class AI:
    
    def __init__(self):
	self.size = 6
	self.nthMark = ' '
	self.aiMark = 'X'
	self.usrMark = 'O'
	
	self.grid = [ [ self.nthMark for i in range(self.size) ] for i in range(self.size) ]
	# ' ' for nothing, 'X' for AI, 'O' for player(user)
	# self.grid[i][j] points (i+1, j+1)
	
    def main(self):
	self.gridUpdate()
	return self.nextPos()
	
    def nextPos(self):
	# Determine the position AI should throw!
	# Basically, to consider the order of algorithms
	isV = self.isVictory()
	isD = self.isDanger()
	
	if isV:
	    return isV
	elif isD:
	    return isD
	else:
	    return self.bestWay()
	    
	
    def gridUpdate(self):
	self.gridRow = self.grid
	self.gridCol = [ [ self.grid[i][j] for i in range(self.size) ] for j in range(self.size) ] 
	
    def isVictory(self):
	# Is there any place that if AI add one stone, AI wins.
	pass
    
    def isDanger(self):
	# Is there any place that if AI ignores, AI loses.
	for i in range(self.size):
	    if self.nthMark in self.gridRow[i] and self.gridRow[i].count(self.usrMark) == self.size-1:
		x = i
		y = self.gridRow[i].index(self.nthMark)
		return [x,y]
	    elif self.nthMark in self.gridCol[i] and self.gridCol[i].count(self.usrMark) == self.size-1:
		x = self.gridCol[i].index(self.nthMark)
		y = i
		return [x,y]
	    
	return 0
	
    def bestWay(self):
	# Find the best place
	return [randint(0,self.size-1), randint(0,self.size-1)]