import os
import numpy as n

def Connection(Map,colx,rowx,coly,rowy):
	if Map[colx][rowx]^Map[coly][rowy] > 0 and Map[colx][rowx] != 0 and Map[coly][rowy] != 0:
		return True
	else:
		return False

def ShowMap(Map,Status):
	os.system('clear')
	for x in range(len(Map)):
		print Map[x]
	if Status == 0:
		StatusM = ""
	elif Status == 1:
		StatusM = "End"
	elif Status == 2:
		StatusM = "Error : Out of Map Size"
	elif Status == 3:
		StatusM = "Error : There is a stone"
	print StatusM

def SynchronizeMap(Map):
	lencol = len(Map)
	lenrow = len(Map[0])
	Map_View = [[" " for x in range(lencol)] for y in range(lenrow)]
	Map_Process = 0
	for col in range(lencol):
		for row in range(lenrow):
			if Map[col][row] > 0:
				Map_View[col][row] = "O"
				Map_Process += 1
			elif Map[col][row] < 0 :
				Map_View[col][row] = "X"
				Map_Process += 1
	if Map_Process == lencol*lenrow:
		Map_Process = -1
	else:
		Map_Process = 0
	return (Map, Map_View, Map_Process)

def CheckGameOver(Map,col,row):
	lenmap = len(Map)
	for Checker in range(lenmap):
		if Checker == lenmap - 1:
			return True
		elif not Connection(Map,Checker,row-1,Checker+1,row-1):
			break
	for Checker in range(lenmap):
		if Checker == lenmap - 1:
			return True
		elif not Connection(Map,col-1,Checker,col-1,Checker+1):
			break
	for Checker in range(lenmap-abs(col-row)):
		if Checker == lenmap-abs(col-row)-1 and lenmap-abs(col-row) != 1:
			return True
		elif lenmap-abs(col-row) != 1 and col < row and not Connection(Map,Checker,row-col+Checker,Checker+1,row-col+Checker+1):
				break
		elif lenmap-abs(col-row) != 1 and col >= row and not Connection(Map,col-row+Checker,Checker,col-row+Checker+1,Checker+1):
				break
	for Checker in range(lenmap-abs(lenmap+1-col-row)):
		if Checker == lenmap-abs(lenmap+1-col-row)-1 and lenmap-abs(lenmap+1-col-row) != 1:
			return True
		elif col > lenmap+1-row:
			if not Connection(Map,col+row-lenmap-1+Checker,lenmap-1-Checker,col+row-lenmap-1+Checker+1,lenmap-1-Checker-1):
				break
		elif col <= lenmap+1-row:
			if not Connection(Map,Checker,col+row-1-Checker-1,Checker+1,col+row-1-Checker-1-1):
				break
