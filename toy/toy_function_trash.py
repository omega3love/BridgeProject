import os
import numpy as n

def ShowMap(Map, Status = 0):
	os.system('clear')
	print Map
	if Status == 0:
		StatusMessage = " "
	elif Status == 1:
		StatusMessage = "Victory!"
	elif Status == 2:
		StatusMessage = "Out of Map Size"
	elif Status == 3:
		StatusMessage = "There is a stone"
	print StatusMessage

def NCheckConnection(Map,Marx1,Mary1,Marx2,Mary2):
	if Map[Marx1][Mary1]^Map[Marx2][Mary2] > 0 and Map[Marx1][Mary1] != 0 and Map[Marx2][Mary2] != 0:
		return False
	else:
		return True

def CheckVictory(Map, Marx, Mary):
	for Checker in range(len(Map)):
		if Checker == len(Map) - 1:
			return True
		elif NCheckConnection(Map,Checker,Mary-1,Checker+1,Mary-1):
			break
	for Checker in range(len(Map)):
		if Checker == len(Map) - 1:
			return True
		elif NCheckConnection(Map,Marx-1,Checker,Marx-1,Checker+1):
			break
	if abs(Marx - Mary) < len(Map) - 1:
		for Checker in range(len(Map) - abs(Marx - Mary)):
			if Checker == len(Map) - abs(Marx - Mary) - 1:
				return True
			elif Mary > Marx:
				if NCheckConnection(Map,Checker,Mary-Marx+Checker,Checker+1,Mary-Marx+Checker+1):
					break
			elif Mary <= Marx:
				if NCheckConnection(Map,Marx-Mary+Checker,Checker,Marx-Mary+Checker+1,Checker+1):
					break
	if abs(len(Map) + 1 - Marx - Mary) < len(Map) - 1:
		for Checker in range(len(Map) - abs(len(Map) + 1 - Marx - Mary)):
			if Checker == len(Map) - abs(len(Map) + 1 - Marx - Mary) - 1:
					return True
			elif Marx > len(Map) + 1 - Mary:
				if NCheckConnection(Map,Marx+Mary-len(Map)-1+Checker,len(Map)-1-Checker,Marx+Mary-len(Map)-1+Checker+1,len(Map)-1-Checker-1):
					break
			elif Marx <= len(Map) + 1 - Mary:
				if NCheckConnection(Map,Checker,Marx+Mary-2-Checker,Checker+1,Marx+Mary-2-Checker-1):
					break
	return False

def CheckEnd(Map):
	MapChecker = 0
	for Checker_col in range(len(Map)):
		for Checker_row in range(len(Map[0])):
			if Map[Checker_col][Checker_row] != 0:
				MapChecker += 1
	if MapChecker == len(Map) * len(Map[0]):
		return True
	else:
		return False

def CheckWinner(Map):
	return 0