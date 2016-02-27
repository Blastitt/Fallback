#!/usr/local/env python

import random as rand
import curses
import time
from datetime import datetime

stdscr = 0
n_win = 0
width = 16
height = 16
mat_game = []

# create 1D array containing game cells
def init_mat(mat_game, width, height):
	mat_game = [(1 if rand.randint(0, 100) < 20 else 0) for x in range(width * height)]
	return mat_game
	
def draw_grid(n_win, mat_game, width, height):
	count = 0
#	n_win.clear()
	for i in mat_game:
		count += 1
#		n_win.addch(' ')
#		n_win.addch(str(i) if i == 1 else ' ')
		print (str(i) if i == 1 else 'o'),
#		n_win.addch(' ')
		if count % height == 0:
#			n_win.addch('\n')
			print '\n'
#	n_win.refresh()
		
def calc_grid(mat_game, width, height):


	for i in range(width * height):
		
		n_cells = 0
		
		# check top neighbor
		if int(i / height) > 0:
			if mat_game[int((i / height - 1) + (i % height))] == 1:
				n_cells += 1
			
			# check top left neighbor
			if int(i % height) > 0 and mat_game[int((i / height - 1) + ((i % height) - 1))] == 1:
				n_cells += 1	
			# check top right neighbor
			if int(i % height) < width - 1 and mat_game[int((i / height - 1) + ((i % height) + 1))] == 1:
				n_cells += 1
						
		# check bottom neighbor
		if int(i / height) < width - 1:
			if mat_game[int((i / height + 1) + (i % height))] == 1:
				n_cells += 1
			
			# check bottom left neighbor
			if int(i % height) > 0 and mat_game[int((i / height + 1) + ((i % height) - 1))] == 1:
				n_cells += 1			
			# check bottom right neighbor
			if int(i % height) < height - 1 and mat_game[int((i / height + 1) + ((i % height) + 1))] == 1:
				n_cells += 1

		# check left neighbor
		if int(i % height) > 0:
			if mat_game[int((i / height) + ((i % height) - 1))] == 1:
				n_cells += 1	
		# check right neighbor
		if int(i % height) < height - 1:
			if mat_game[int((i / height) + ((i % height) + 1))] == 1:
				n_cells += 1


		if mat_game[int((i / height) + (i % height))] == 0 and n_cells == 3:
			mat_game[int((i / height) + (i % height))] = 1
		if n_cells < 2 or n_cells > 3:
			mat_game[int((i / height) + (i % height))] = 0
	
	return mat_game

# init curses
'''stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)
n_win = curses.newwin(50, 50, 0, 0)
'''

mat_game = init_mat(mat_game, width, height)
'''
while(True):
	mat_game = calc_grid(mat_game, width, height)
	draw_grid(n_win, mat_game, width, height)
	time.sleep(0.1)
'''

draw_grid(n_win, mat_game, width, height)
print '----------------'
mat_game2 = calc_grid(mat_game, width, height)
draw_grid(n_win, mat_game2, width, height)
print '----------------'
mat_game3 = calc_grid(mat_game2, width, height)
draw_grid(n_win, mat_game3, width, height)

# end curses
'''curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()'''
