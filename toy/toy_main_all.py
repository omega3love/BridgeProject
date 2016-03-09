#! /usr/bin/python

#Import
import pygame
import os
import operator
import random

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
	pygame.display.set_mode((100,100))

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
				#Get Arrow KEY
				sys_wait, game_position = GetArrowKeys(event, game_position)
				#Get Space KEY
				if event.key == pygame.K_SPACE:
					game_map, game_last_position, game_turn = ThrowStone(game_map, game_position, game_turn)
					sys_stat = str(game_last_position)
				#Get AI KEY
				if event.key == pygame.K_TAB:
					game_position = aikey(game_map,game_turn)
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
	count1_value = [0,0,0]
	count2_value = [0,0,0]
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
						for seeding in xrange(1,seed+1):
							end_map[0][x+seeding][y] = '%d' %(seed+1)
					elif end_map[0][x][y] == 'seed' and IsConnected_X(Map,[x,y],[x+seed,y]):
						for seeding in xrange(1,seed+1):
							end_map[0][x+seeding][y] = '%d' %(-seed-1)
					else:
						break
		for x in xrange(6):
			for y in xrange(6):
				for seed in xrange(1,6-y):
					if end_map[1][x][y] == 'seed' and IsConnected_O(Map,[x,y],[x,y+seed]):
						for seeding in xrange(1,seed+1):
							end_map[1][x][y+seeding] = '%d' %(seed+1)
					elif end_map[1][x][y] == 'seed' and IsConnected_X(Map,[x,y],[x,y+seed]):
						for seeding in xrange(1,seed+1):
							end_map[1][x][y+seeding] = '%d' %(-seed-1)
					else:
						break
		for x in xrange(6):
			for y in xrange(6):
				if 5>x>y:
					for seed in xrange(1,5-x):
						if end_map[2][x][y] == 'seed' and IsConnected_O(Map,[x,y],[x+seed,y+seed]):
							for seeding in xrange(1,seed+1):
								end_map[2][x+seeding][y+seeding] = '%d' %(seed+1)
						elif end_map[2][x][y] == 'seed' and IsConnected_X(Map,[x,y],[x+seed,y+seed]):
							for seeding in xrange(1,seed+1):
								end_map[2][x+seeding][y+seeding] = '%d' %(-seed-1)
						else:
							break
				if x<=y<5:
					for seed in xrange(1,5-y):
						if end_map[2][x][y] == 'seed' and IsConnected_O(Map,[x,y],[x+seed,y+seed]):
							for seeding in xrange(1,seed+1):
								end_map[2][x+seeding][y+seeding] = '%d' %(seed+1)
						elif end_map[2][x][y] == 'seed' and IsConnected_X(Map,[x,y],[x+seed,y+seed]):
							for seeding in xrange(1,seed+1):
								end_map[2][x+seeding][y+seeding] = '%d' %(-seed-1)
						else:
							break
		for x in xrange(6):
			for y in xrange(6):
				if 5>x>5-y:
					for seed in xrange(1,5-x):
						if end_map[3][x][y] == 'seed' and IsConnected_O(Map,[x,y],[x+seed,y-seed]):
							for seeding in xrange(1,seed+1):
								end_map[3][x+seeding][y-seeding] = '%d' %(seed+1)
						elif end_map[3][x][y] == 'seed' and IsConnected_X(Map,[x,y],[x+seed,y-seed]):
							for seeding in xrange(1,seed+1):
								end_map[3][x+seeding][y-seeding] = '%d' %(-seed-1)
						else:
							break
				if x<=5-y<5:
					for seed in xrange(1,y):
						if end_map[3][x][y] == 'seed' and IsConnected_O(Map,[x,y],[x+seed,y-seed]):
							for seeding in xrange(1,seed+1):
								end_map[3][x+seeding][y-seeding] = '%d' %(seed+1)
						elif end_map[3][x][y] == 'seed' and IsConnected_X(Map,[x,y],[x+seed,y-seed]):
							for seeding in xrange(1,seed+1):
								end_map[3][x+seeding][y-seeding] = '%d' %(-seed-1)
						else:
							break
		for z in xrange(4):
			for x in xrange(6):
				count1_value[0] += end_map[z][x].count('5')
				count2_value[0] += end_map[z][x].count('-5')
				count1_value[1] += end_map[z][x].count('4')
				count2_value[1] += end_map[z][x].count('-4')
				count1_value[2] += end_map[z][x].count('3')
				count2_value[2] += end_map[z][x].count('-3')
		for x in xrange(3):
			count1_value[x] = count1_value[x]/(4-x)
			count2_value[x] = count2_value[x]/(4-x)
		print count1_value
		print count2_value
		if count1_value[0]>count2_value[0]:
			return 1
		elif count1_value[0]<count2_value[0]:
			return 2
		else:
			if count1_value[1]>count2_value[1]:
				return 1
			elif count1_value[1]<count2_value[1]:
				return 2
			else:
				if count1_value[2]>count2_value[2]:
					return 1
				elif count1_value[2]<count2_value[2]:
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

#AI Function
def aikey(Map, turn, winning=[1,0.5,0.5], losing=[1,0.5]):
	#Declare Values
	position_value = [0 for x in xrange(5)]
	position_index = 0
	position_box = []
	return_position = [[-1,-1]for x in xrange(5)]
	virtual_map = [[' 'for x in xrange(6)]for y in xrange(6)]
	winning_1st = winning[0]
	winning_2nd = winning[1]
	winning_3rd = winning[2]
	losing_1st = losing[0]
	losing_2nd = losing[1]
	#Initialize
	for x in xrange(6):
		for y in xrange(6):
			virtual_map[x][y] = Map[x][y]
	if turn:
		df_position = 'X'
		at_position = 'O'
	if not turn:
		df_position = 'O'
		at_position = 'X'
	#Defence Losing Position
	#Defence First Order Losing Position
	for x in xrange(6):
		for y in xrange(6):
			if virtual_map[x][y] == ' ':
				virtual_map[x][y] = df_position
				if IsEnded_Bridge(virtual_map,[x,y]):
					position_box.append("[%d,%d]"%(x,y))
					position_value[0] = losing_1st
				virtual_map[x][y] = ' '
	return_position[0] = aipositionbox(position_box)
	position_box = []
	#Defence Second Order Losing Position
	for x in xrange(6):
		for y in xrange(6):
			if virtual_map[x][y] == ' ':
				virtual_map[x][y] = df_position
				if not IsEnded_Bridge(virtual_map,[x,y]):
					for z in xrange(6):
						for w in xrange(6):
							if z != x and w != y and Map[z][w] == ' ':
								virtual_map[z][w] = df_position
								if IsEnded_Bridge(virtual_map,[z,w]):
									position_box.append("[%d,%d]"%(x,y))
									position_value[1] = losing_2nd
								virtual_map[z][w] = ' '
				virtual_map[x][y] = ' '
	return_position[1] = aipositionbox(position_box)
	position_box = []
	#Attack Winning Position
	#Attack Third Order Winning Position
	for x in xrange(6):
		for y in xrange(6):
			if virtual_map[x][y] == ' ':
				virtual_map[x][y] = at_position
				if not IsEnded_Bridge(virtual_map,[x,y]):
					for z in xrange(6):
						for w in xrange(6):
							if z != x and w != y and Map[z][w] == ' ':
								virtual_map[z][w] = at_position
								if not IsEnded_Bridge(virtual_map,[z,w]):
									for a in xrange(6):
										for b in xrange(6):
											if a != x and a != z and b != y and b != w and virtual_map[a][b] == ' ':
												virtual_map[a][b] = at_position
												if IsEnded_Bridge(virtual_map,[a,b]):
													position_box.append("[%d,%d]"%(x,y))
													position_value[2] = winning_3rd
												virtual_map[a][b] = ' '
								virtual_map[z][w] = ' '
				virtual_map[x][y] = ' '
	return_position[2] = aipositionbox(position_box)
	position_box = []
	#Attack Second Order Winning Position
	for x in xrange(6):
		for y in xrange(6):
			if virtual_map[x][y] == ' ':
				virtual_map[x][y] = at_position
				if not IsEnded_Bridge(virtual_map,[x,y]):
					for z in xrange(6):
						for w in xrange(6):
							if z != x and w != y and Map[z][w] == ' ':
								virtual_map[z][w] = at_position
								if IsEnded_Bridge(virtual_map,[z,w]):
									position_box.append("[%d,%d]"%(x,y))
									position_value[3] = winning_2nd
								virtual_map[z][w] = ' '
				virtual_map[x][y] = ' '
	return_position[3] = aipositionbox(position_box)
	position_box = []
	#Attack First Order Winning Position
	for x in xrange(6):
		for y in xrange(6):
			if virtual_map[x][y] == ' ':
				virtual_map[x][y] = at_position
				if IsEnded_Bridge(virtual_map,[x,y]):
					position_box.append("[%d,%d]"%(x,y))
					position_value[4] = winning_1st
				virtual_map[x][y] = ' '
	return_position[4] = aipositionbox(position_box)
	position_box = []
	#Evaluate position_value
	if position_value[4] == 1:
		return return_position[4]
	elif position_value[0] == 1:
		return return_position[0]
	elif not position_value == [0 for x in xrange(5)]:
		for x in xrange(5):
			if position_value[x] == 1:
				position_value[x] = 0
		position_value[x] = random.random()*position_value[x]
		position_index = int(max(enumerate(position_value),key=operator.itemgetter(1))[0])
		return return_position[position_index]
	else:
		while True:
			return_position[0] = eval("[random.randrange(0,len(Map)),random.randrange(0,len(Map[0]))]")
			if Map[return_position[0][0]][return_position[0][1]] == ' ':
				break
		return return_position[0]
def aipositionbox(box):
	if len(box) != 0:
		random_position = box[random.randrange(0,len(box))]
		return eval(random_position)


#Exe
if __name__ == "__main__":
	Main()