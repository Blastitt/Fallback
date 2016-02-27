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
def init_mat(matrix, width, height):
	matrix = [(1 if rand.randint(0, 100) < 15 else 0) for x in range(width * height)]
	return matrix
	
def draw_grid(n_win, matrix, width, height):
	count = 0
	n_win.clear()
	for i in matrix:
		count += 1
		n_win.addch(' ')
		n_win.addch('x' if i == 1 else ' ')
		n_win.addch(' ')
		if count % height == 0:
			n_win.addch('\n')
	n_win.refresh()
		
def calc_grid(matrix, width, height):

	for i in range(width * height):
		
		n_cells = 0
		
		# check top neighbor
		if int(i / height) > 0:
			if matrix[int(((i / height - 1) * height) + (i % height))] == 1:
				n_cells += 1
			
			# check top left neighbor
			if int(i % height) > 0 and matrix[int(((i / height - 1) * height) + ((i % height) - 1))] == 1:
				n_cells += 1	
			# check top right neighbor
			if int(i % height) < width - 1 and matrix[int(((i / height - 1) * height) + ((i % height) + 1))] == 1:
				n_cells += 1
						
		# check bottom neighbor
		if int(i / height) < width - 1:
			if matrix[int(((i / height + 1) * height) + (i % height))] == 1:
				n_cells += 1
			
			# check bottom left neighbor
			if int(i % height) > 0 and matrix[int(((i / height + 1) * height) + ((i % height) - 1))] == 1:
				n_cells += 1			
			# check bottom right neighbor
			if int(i % height) < height - 1 and matrix[int(((i / height + 1) * height) + ((i % height) + 1))] == 1:
				n_cells += 1

		# check left neighbor
		if int(i % height) > 0:
			if matrix[int((i / height * height) + ((i % height) - 1))] == 1:
				n_cells += 1	
		# check right neighbor
		if int(i % height) < height - 1:
			if matrix[int((i / height * height) + ((i % height) + 1))] == 1:
				n_cells += 1


		if matrix[i] == 0 and n_cells == 3:
			matrix[i] = 1
		if n_cells < 2 or n_cells > 3:
			matrix[i] = 0

	return matrix
def main():
	# init curses
	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	stdscr.keypad(1)
	n_win = curses.newwin(50, 50, 0, 0)

	m_game = init_mat(mat_game, width, height)
	while(True):
		m_game = calc_grid(m_game, width, height)
		draw_grid(n_win, m_game, width, height)
		time.sleep(0.1)

	# end curses
	curses.nocbreak()
	stdscr.keypad(0)
	curses.echo()
	curses.endwin()

if __name__ == '__main__':
	main()
