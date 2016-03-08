#! /usr/bin/python

#Import
import pygame
import os

#Main Function
def Main():
	pygame.init()
	#declare values
	game_map = [[' 'for x in xrange(6)]for y in xrange(6)]
	game_position = [2,2]
	game_last_position = [0,0]
	game_turn = True
	game_End = [False,0]
	sys_wait = 0
	sys_stat = 'Game Start!'

	#While Loop
	while True:
		#Show Map
		sys_wait = ShowMap(game_map,game_position,game_turn,sys_wait,sys_stat)
			#Get Events
		for event in pygame.event.get():
			#QUIT Game
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
			#Get KEY
			if event.type == pygame.KEYUP and game_End == [False,0]:
				sys_wait, game_position = GetArrowKeys(event, game_position)
				if event.key == pygame.K_SPACE:
					game_map, game_last_position, game_turn = ThrowStone(game_map, game_position, game_turn)
					sys_stat = str(game_last_position)
		#Check Victory Conditions
		game_End = IsEnded(game_map,game_last_position)
		sys_stat, sys_wait = IsEnded_System(game_End,sys_wait,sys_stat,game_turn)

#Show Map
def ShowMap(Map, position, turn, wait, stat):
	pygame.time.wait(20)
	if wait < 10:
		ShowMap_WP(Map,position,turn)
		wait += 1
	elif wait < 20:
		ShowMap_NP(Map)
		wait += 1
	else:
		ShowMap_WP(Map,position,turn)
		wait = 1
	print stat
	return wait
def ShowMap_NP(Map):
	os.system('clear')
	view_map = [['V'for x in xrange(len(Map))]for y in xrange(len(Map[0]))]
	for x in xrange(len(Map)):
		for y in xrange(len(Map[0])):
				view_map[x][y] = Map[x][y]
	for x in xrange(len(Map)):
		print view_map[x]
def ShowMap_WP(Map, position, turn):
	os.system('clear')
	view_map = [['V'for x in xrange(len(Map))]for y in xrange(len(Map[0]))]
	for x in xrange(len(Map)):
		for y in xrange(len(Map[0])):
			if x == position[0] and y == position[1]:
				if turn and not 'O' in Map[x][y]:
					view_map[x][y] = 'O'
				elif not turn and not 'X' in Map[x][y]:
					view_map[x][y] = 'X'
				else:
					view_map[x][y] = ' '
			else:
				view_map[x][y] = Map[x][y]
	for x in xrange(len(Map)):
		print view_map[x]

#Get Arrow Keys
def GetArrowKeys(event, position):
	if event.key == pygame.K_UP:
		position[0] -= 1
	if event.key == pygame.K_DOWN:
		position[0] += 1
	if event.key == pygame.K_LEFT:
		position[1] -= 1
	if event.key == pygame.K_RIGHT:
		position[1] += 1
	position[0] = position[0] % 6
	position[1] = position[1] % 6
	return 1, position

#Throw Stone
def ThrowStone(Map, position, turn):
	if Map[position[0]][position[1]] == ' ':
		if turn:
			Map[position[0]][position[1]] = "O"
			turn = False
		else:
			Map[position[0]][position[1]] = "X"
			turn = True
	return Map, position, turn

#Is Ended
def IsEnded(Map, position):
	return [IsEnded_Bridge(Map, position), IsEnded_FullMap(Map)]
#Is Ended Bridge
def IsEnded_Bridge(Map, position):
	for seed in xrange(6):
		if seed == 5:
			return True
		elif not IsConnected_col(Map, position, seed):
			break
	for seed in xrange(6):
		if seed == 5:
			return True
		elif not IsConnected_row(Map, position, seed):
			break
	for seed in xrange(6-abs(position[0]-position[1])):
		if seed == 5-abs(position[0]-position[1]) and abs(position[0]-position[1]) != 5:
			return True
		elif position[0] > position[1] and position[0]-position[1] < 5:
			position_init = [position[0]-position[1],0]
			if not IsConnected_lor(Map, position_init, seed):
				break
		elif position[0] <= position[1] and position[0]-position[1] > -5:
			position_init = [0,-position[0]+position[1]]
			if not IsConnected_lor(Map, position_init, seed):
				break
	for seed in xrange(6-abs(5-position[0]-position[1])):
		if seed == 5-abs(5-position[0]-position[1]) and abs(5-position[0]-position[1]) != 5:
			return True
		elif position[0] > 5-position[1] and position[0]+position[1] < 10:
			position_init = [-5+position[0]+position[1],5]
			if not IsConnected_lol(Map, position_init, seed):
				break
		elif position[0] <= 5-position[1] and position[0]+position[1] > 0:
			position_init = [0,position[0]+position[1]]
			if not IsConnected_lol(Map, position_init, seed):
				break
	return False
def IsConnected_col(Map, position, seed):
	if Map[seed][position[1]] == Map[seed+1][position[1]] and Map[seed][position[1]] != ' ':
		return True
	else:
		return False
def IsConnected_row(Map, position, seed):
	if Map[position[0]][seed] == Map[position[0]][seed+1] and Map[position[0]][seed] != ' ':
		return True
	else:
		return False
def IsConnected_lor(Map, position, seed):
	if Map[position[0]+seed][position[1]+seed] == Map[position[0]+seed+1][position[1]+seed+1] and Map[position[0]+seed][position[1]+seed] != ' ':
		return True
	else:
		return False
def IsConnected_lol(Map, position, seed):
	if Map[position[0]+seed][position[1]-seed] == Map[position[0]+seed+1][position[1]-seed-1] and Map[position[0]+seed][position[1]-seed] != ' ':
		return True
	else:
		return False
#IsEnded Full Map
def IsEnded_FullMap(Map):
	search_value = 0
	for x in xrange(6):
		for y in xrange(6):
			if Map[x][y] == ' ':
				return 0
			else:
				search_value += 1
	end_map = [[['seed'for x in xrange(6)]for y in xrange(6)]for z in xrange(4)]
	if search_value == 36:
		for x in xrange(6):
			for y in xrange(6):
				for seed in xrange(1,6-x):
					if end_map[0][x][y] == 'seed' and IsConnected_O(Map,[x,y],[x+seed,y]):
						end_map[0][x+seed][y] = '%d' %(seed+1)
					if end_map[0][x][y] == 'seed' and IsConnected_X(Map,[x,y],[x+seed,y]):
						end_map[0][x+seed][y] = '%d' %(-seed-1)
					else:
						break
		for x in xrange(6):
			for y in xrange(6):
				for seed in xrange(1,6-y):
					if end_map[1][x][y] == 'seed' and IsConnected_O(Map,[x,y],[x,y+seed]):
						end_map[1][x][y+seed] = '%d' %(seed+1)
					if end_map[1][x][y] == 'seed' and IsConnected_X(Map,[x,y],[x,y+seed]):
						end_map[1][x][y+seed] = '%d' %(-seed-1)
					else:
						break
		for x in xrange(6):
			for y in xrange(6):
				if 5>x>y:
					for seed in xrange(1,5-x):
						if end_map[2][x][y] == 'seed' and IsConnected_O(Map,[x,y],[x+seed,y+seed]):
							end_map[2][x+seed][y+seed] = '%d' %(seed+1)
						if end_map[2][x][y] == 'seed' and IsConnected_X(Map,[x,y],[x+seed,y+seed]):
							end_map[2][x+seed][y+seed] = '%d' %(-seed-1)
						else:
							break
				if x<=y<5:
					for seed in xrange(1,5-y):
						if end_map[2][x][y] == 'seed' and IsConnected_O(Map,[x,y],[x+seed,y+seed]):
							end_map[2][x+seed][y+seed] = '%d' %(seed+1)
						if end_map[2][x][y] == 'seed' and IsConnected_X(Map,[x,y],[x+seed,y+seed]):
							end_map[2][x+seed][y+seed] = '%d' %(-seed-1)
						else:
							break
		for x in xrange(6):
			for y in xrange(6):
				if 5>x>5-y:
					for seed in xrange(1,5-x):
						if end_map[3][x][y] == 'seed' and IsConnected_O(Map,[x,y],[x+seed,y-seed]):
							end_map[3][x+seed][y-seed] = '%d' %(seed+1)
						if end_map[3][x][y] == 'seed' and IsConnected_X(Map,[x,y],[x+seed,y-seed]):
							end_map[3][x+seed][y-seed] = '%d' %(-seed-1)
						else:
							break
				if x<=5-y<5:
					for seed in xrange(1,y):
						if end_map[3][x][y] == 'seed' and IsConnected_O(Map,[x,y],[x+seed,y-seed]):
							end_map[3][x+seed][y-seed] = '%d' %(seed+1)
						if end_map[3][x][y] == 'seed' and IsConnected_X(Map,[x,y],[x+seed,y-seed]):
							end_map[3][x+seed][y-seed] = '%d' %(-seed-1)
						else:
							break
		for z in xrange(4):
			for y in xrange(6):
				print end_map[z][x]
		if end_map.count('5')>end_map.count('-5'):
			return 1
		elif end_map.count('5')<end_map.count('-5'):
			return 2
		else:
			if end_map.count('4')>end_map.count('-4'):
				return 1
			elif end_map.count('4')<end_map.count('-4'):
				return 2
			else:
				if end_map.count('3')>end_map.count('-3'):
					return 1
				elif end_map.count('3')<end_map.count('-3'):
					return 2
				else:
					return 3
def IsConnected_O(Map, position1, position2):
	if Map[position1[0]][position1[1]] == Map[position2[0]][position2[1]] and Map[position1[0]][position1[1]] == 'O':
		return True
	else:
		return False
def IsConnected_X(Map, position1, position2):
	if Map[position1[0]][position1[1]] == Map[position2[0]][position2[1]] and Map[position1[0]][position1[1]] == 'X':
		return True
	else:
		return False
#IsEnded System
def IsEnded_System(End, wait, stat, turn):
	return_stat = ' '
	return_wait = 11
	if End == [True,0]:
		if not turn:
			return_stat = 'Win player : player 1 (O)'
		if turn:
			return_stat = 'Win player : player 2 (X)'
	elif not End[0] and End[1] != 0:
		if End[1] == 1:
			return_stat = 'Win player : player 1 (O)'
		if End[1] == 2:
			return_stat = 'Win player : player 2 (X)'
		if End[1] == 3:
			return_stat = 'Draw'
	else:
		return_stat = stat
		return_wait = wait
	return return_stat, return_wait


#Exe
if __name__ == "__main__":
	Main()