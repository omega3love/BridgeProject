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
		Map_CEnd = True
	else:
		Map_CEnd = False
	return (Map_View, Map_CEnd)

def IsEnded_C(Map,col,row):
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
<<<<<<< HEAD
		if Checker == lenmap-abs(col-row)-1 and lenmap-abs(col-row) != 1:
			return True
		elif lenmap-abs(col-row) != 1 and col < row:
			if not Connection(Map,Checker,row-col+Checker,Checker+1,row-col+Checker+1):
				break
		elif lenmap-abs(col-row) != 1 and col >= row:
			if not Connection(Map,col-row+Checker,Checker,col-row+Checker+1,Checker+1):
				break
	for Checker in range(lenmap-abs(lenmap+1-col-row)):
		if Checker == lenmap-abs(lenmap+1-col-row)-1 and lenmap-abs(lenmap+1-col-row) != 1:
			return True
		elif col > lenmap+1-row:
			if not Connection(Map,col+row-lenmap+Checker,lenmap-1-Checker,col+row-lenmap+Checker+1,lenmap-1-Checker-1):
				break
		elif col <= lenmap+1-row:
			if not Connection(Map,Checker,col+row-2-Checker,Checker+1,col+row-2-Checker-1):
				break
=======
		if lenmap-abs(col-row) > 1:
			if Checker == lenmap-abs(col-row)-1:
				return True
			elif col < row:
				if not Connection(Map,Checker,row-col+Checker,Checker+1,row-col+Checker+1):
					break
			elif col >= row:
				if not Connection(Map,col-row+Checker,Checker,col-row+Checker+1,Checker+1):
					break
	for Checker in range(lenmap-abs(lenmap+1-col-row)):
		if 2 < col+row < lenmap*2:
			if Checker == lenmap-abs(lenmap+1-col-row)-1:
				return True
			elif col > lenmap+1-row:
				if not Connection(Map,col+row-lenmap-1+Checker,lenmap-1-Checker,col+row-lenmap+Checker,lenmap-1-Checker-1):
					break
			elif col <= lenmap+1-row:
				if not Connection(Map,Checker,col+row-2-Checker,Checker+1,col+row-2-Checker-1):
					break
	return False
      

def CheckWinner(Map):
	return 0
>>>>>>> c93859e5169c2b20f7991afe448f4d8f9ffdfeca
