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

def CheckVictory(Map, Marx, Mary):
	for Checker in range(6):
		if Checker == 5:
			return True
		elif Map[Checker][Marx - 1]*Map[Checker + 1][Mary - 1] <= 0:
			break
	for Checker in range(6):
		if Checker == 5:
			return True
		elif Map[Marx - 1][Checker]*Map[Marx - 1][Checker + 1] <= 0:
			break
	if abs(Marx - Mary) < 5:
		for Checker in range(6 - abs(Marx - Mary)):
			if Checker == 6 - abs(Marx - Mary) - 1:
				return True
			elif Mary > Marx:
				if Map[Checker][Mary - Marx + Checker]*Map[Checker + 1][Mary - Marx + Checker + 1] <= 0:
					break
			elif Mary <= Marx:
				if Map[Marx - Mary + Checker][Checker]*Map[Marx - Mary + Checker + 1][Checker + 1] <= 0:
					break
	if abs(7 - Marx - Mary) < 5:
		for Checker in range(6 - abs(7 - Marx - Mary)):
			if Checker == 6 - abs(7 - Marx - Mary) - 1:
						return True
			elif Marx > 7 - Mary:
				if Map[Marx + Mary - 7 + Checker][5 - Checker]*Map[Marx + Mary - 7 + Checker + 1][5 - Checker - 1] <= 0:
					break
			elif Marx <= 7 - Mary:
				if Map[Checker][Marx + Mary - 2 - Checker]*Map[Checker + 1][Marx + Mary - 2 - Checker - 1] <= 0:
					break
	return False