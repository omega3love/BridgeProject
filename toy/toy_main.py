#! /usr/bin/python

# Main Game

# Import
import numpy as n
from toy_function import *

# Preset
Map = n.zeros((6,6),dtype=n.int)
End = False
Status = 0
Turn = True
Nurn = 0

# Background Loop
while not End:
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
# Check victory 1
			End = CheckVictory(Map, markerx, markery)
# Player 2
		elif Map[markerx - 1][markery - 1] == 0 and not Turn:
			Nurn += 1
			Map[markerx - 1][markery - 1] = -Nurn
			Turn = True
# Check victory 2
			End = CheckVictory(Map, markerx, markery)
# Check error
		else:
			Status = 3
	else:
		Status = 2
Status = 1
ShowMap(Map, Status)
if not Turn:
	print "Win Player : Player 1"
elif Turn:
	print "Win Player : Player 2"