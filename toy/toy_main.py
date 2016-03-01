#! /usr/bin/python

# Main Game

# Import
import numpy as n
from toy_function import *

# Preset
Map = n.zeros((6,6),dtype=n.int)
GEnd = False
CEnd = False
Status = 0
Turn = True
Nurn = 0

# Background Loop
while not GEnd or CEnd:
# Show Map
	ShowMap(Map, Status)
# Print Player's Turn
	if Turn:
		print "Player 1"
	else:
		print "Player 2"
# Input Stone position
	markerx = input("Marker x : ")
	markery = input("Marker y : ")
# Check Stone and Add Stone
# Player 1
	if 0 < markerx <= 6 and 0 < markery <=6:
		if Map[markerx - 1][markery - 1] == 0 and Turn:
			Nurn += 1
			Map[markerx - 1][markery - 1] = Nurn
			Turn = False
			Status = 0
# Check victory 1
			End = CheckVictory(Map, markerx, markery)
# Player 2
		elif Map[markerx - 1][markery - 1] == 0 and not Turn:
			Nurn += 1
			Map[markerx - 1][markery - 1] = -Nurn
			Turn = True
			Status = 0
# Check victory 2
			GEnd = CheckVictory(Map, markerx, markery)
			CEnd = CheckEnd(Map)
# Check error
		else:
			Status = 3
	else:
		Status = 2
Status = 1
if GEnd:
	ShowMap(Map, Status)
	if not Turn:
		print "Win Player : Player 1"
	elif Turn:
		print "Win Player : Player 2"
elif CEnd:
	ShowMap(Map, Status)
	if CheckWinner(Map) == 1:
		print "Win Player : Player 1"
	elif CheckWinner(Map) == 2:
		print "Win Player : Player 2"
	else:
		print "Draw"