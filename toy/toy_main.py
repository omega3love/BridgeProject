#! /usr/bin/python

# Main Game

# Import
import numpy as n
from toy_functions import *

# Preset
Mapsize = input("Map Size : ")
Map_Sys = n.zeros((Mapsize,Mapsize),dtype=n.int)
GEnd = False
CEnd = False
Status = 0
Turn = True
Nurn = 0
Map_View = [[" " for x in range(Mapsize)] for y in range(Mapsize)]

# Background Loop
while not GEnd:
<<<<<<< HEAD
=======
	Map_View = SynchronizeMap(Map_Sys)[1]
>>>>>>> c93859e5169c2b20f7991afe448f4d8f9ffdfeca
# Show Map
	ShowMap(Map_View, Status)
# Print Player's Turn
	if Turn:
		print "Player 1"
	elif not Turn:
		print "Player 2"
# Input Stone position
	markerx = input("Marker x : ")
	markery = input("Marker y : ")
# Check Stone and Add Stone
# Player 1
	if 0 < markerx <= Mapsize and 0 < markery <= Mapsize:
		if Map_Sys[markerx - 1][markery - 1] == 0 and Turn:
			Nurn += 1
			Map_Sys[markerx - 1][markery - 1] = Nurn
			Turn = False
			Status = 0
<<<<<<< HEAD
			GEnd = CheckGameOver(Map_Sys, markerx, markery)
			(Map_View,CEnd) = SynchronizeMap(Map_Sys)
=======
			GEnd = IsEnded_C(Map_Sys, markerx, markery)
>>>>>>> c93859e5169c2b20f7991afe448f4d8f9ffdfeca
# Player 2
		elif Map_Sys[markerx - 1][markery - 1] == 0 and not Turn:
			Nurn += 1
			Map_Sys[markerx - 1][markery - 1] = -Nurn
			Turn = True
			Status = 0
<<<<<<< HEAD
			GEnd = CheckGameOver(Map_Sys, markerx, markery)
			(Map_View,CEnd) = SynchronizeMap(Map_Sys)
=======
			GEnd = IsEnded_C(Map_Sys, markerx, markery)
>>>>>>> c93859e5169c2b20f7991afe448f4d8f9ffdfeca
# Check error
		else:
			Status = 3
		if SynchronizeMap(Map_Sys)[2] == Mapsize*Mapsize:
			GEnd = True
			CEnd = True
	else:
		Status = 2
Status = 1
if GEnd and not CEnd:
	Map_View = SynchronizeMap(Map_Sys)[1]
	ShowMap(Map_View, Status)
	if not Turn:
		print "Win Player : Player 1"
	elif Turn:
		print "Win Player : Player 2"
elif GEnd and CEnd:
	Map_View = SynchronizeMap(Map_Sys)[1]
	ShowMap(Map, Status)
	if CheckWinner(Map) == 1:
		print "Win Player : Player 1"
	elif CheckWinner(Map) == 2:
		print "Win Player : Player 2"
	else:
		print "Draw"