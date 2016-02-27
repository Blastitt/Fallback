#!/usr/local/env python

import random as rand
import curses
import time
from datetime import datetime

class Controller:

	def __init__(self, width = 16, height = 16):
		self.stdscr = None
		self.n_win = None
		self.game_width = width
		self.game_height = height
		self.game_matrix = []

	# create 1D array containing game cells
	def init_mat(self, width = None, height = None):
		width = self.game_width if width == None else width
		height = self.game_height if height == None else height
		matrix = [(1 if rand.randint(0, 100) < 15 else 0) for x in range(self.game_width * height)]
		return matrix
		
	def set_game_matrix(self, matrix):
		self.game_matrix = matrix

	def draw_grid(self, n_win, matrix, width = None, height = None):
		width = self.game_width if width == None else width
		height = self.game_height if height == None else height
		
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
			
	def calc_grid(self, matrix, width = None, height = None):
		width = self.game_width if width == None else width
		height = self.game_height if height == None else height

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

	def get_game_data(self):
		game_data = ""
		for i in self.game_matrix:
			game_data += str(i)
		print game_data


def main():
	
	# init curses
	stdscr = curses.initscr()
	curses.noecho()
	curses.cbreak()
	stdscr.keypad(1)
	n_win = curses.newwin(50, 50, 0, 0)

	controller = Controller(16, 16)
	m_game = controller.init_mat()
	while(True):
		m_game = controller.calc_grid(m_game)
		controller.set_game_matrix(m_game)
		controller.draw_grid(n_win, m_game)
		time.sleep(0.1)

	# end curses
	curses.nocbreak()
	stdscr.keypad(0)
	curses.echo()
	curses.endwin()

if __name__ == '__main__':
	main()
