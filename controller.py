#!/usr/bin/env python

import random as rand
import curses
import time
import sys

from datetime import datetime

class Controller:

	def __init__(self, width = 16, height = 16):
		self.stdscr = None
		self.n_win = None
		self.game_width = width
		self.game_height = height
		self.game_matrix = []

		self.red = 0
		self.green = 0
		self.blue = 0


		# init display constants
		self.DISPLAY_TL = 1
		self.DISPLAY_TR = 2
		self.DISPLAY_BL = 3
		self.DISPLAY_BR = 4
		self.DISPLAY_ALL = 5

		self.display_mode = self.DISPLAY_ALL

	# create 1D array containing game cells
	def init_mat(self, width = None, height = None):
		width = self.game_width if width == None else width
		height = self.game_height if height == None else height
		matrix = [(1 if rand.randint(0, 100) < 65 else 0) for x in range(self.game_width * height)]
		return matrix

	def set_display_mode(self, disp_mode):
		self.display_mode = disp_mode

	def set_game_matrix(self, matrix):
		self.game_matrix = matrix

	def set_colors(self, color_str):
		self.red = int(color_str[:4], 16)
		self.green = int(color_str[4:8], 16)
		self.blue = int(color_str[8:12], 16)

	def get_display_mode(self):
		return self.display_mode

	def get_grid_position(self, disp_mode = None):
		disp_mode = self.display_mode if disp_mode == None else disp_mode
		if disp_mode == self.DISPLAY_TL:
			return "TL"
		if disp_mode == self.DISPLAY_TR:
			return "TR"
		if disp_mode == self.DISPLAY_BL:
			return "BL"
		if disp_mode == self.DISPLAY_BR:
			return "BR"
		return "ALL"

	def get_partial_game_width(self):
		if self.display_mode != self.DISPLAY_ALL:
			return self.game_width / 2
		return self.game_width

	def get_partial_game_height(self):
		if self.display_mode != self.DISPLAY_ALL:
			return self.game_height / 2
		return self.game_height

	def get_partial_grid(self, matrix = None, width = None, height = None, disp_mode = None):
		width = self.game_width if width == None else width
		height = self.game_height if height == None else height
		disp_mode = self.display_mode if disp_mode == None else disp_mode
		matrix = self.game_matrix if matrix == None else matrix

		n_width = width
		n_height = height
		n_offset_x = 0
		n_offset_y = 0

		n_matrix = None

		if disp_mode != self.DISPLAY_ALL:
			n_width = width / 2
			n_height = height / 2
			n_matrix = range(n_width * n_height)

			if disp_mode == self.DISPLAY_TR:
				n_offset_y = n_width
			if disp_mode == self.DISPLAY_BL:
				n_offset_x = n_height
			if disp_mode == self.DISPLAY_BR:
				n_offset_y = n_width
				n_offset_x = n_height

			for i in range(width * height):
				n_index = ((i / height - n_offset_x) * n_height) + (i % n_height)
				if ((i / height - n_offset_x)) >= 0 and ((i / height - n_offset_x)) < n_height:
					if i % height - n_offset_y >= 0 and i % height - n_offset_y < n_width:
						n_matrix[n_index] = matrix[i]

			matrix = n_matrix
		return matrix

	def get_color():
		return (self.red << 16) | (self.green << 8) | self.blue


	def draw_grid(self, n_win = None, matrix = None, width = None, height = None):
		width = self.get_partial_game_width() if width == None else width
		height = self.get_partial_game_height() if height == None else height
		n_win = self.n_win if n_win == None else n_win
		matrix = self.game_matrix if matrix == None else matrix

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

		ret_mat = list(matrix)

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
				ret_mat[i] = 1
			if n_cells < 2 or n_cells > 3:
				ret_mat[i] = 0

		return ret_mat

	def get_game_data(self):
		game_data = ""
		game_data += "{0:#0{1}x}".format(self.red,4)
		game_data += "{0:#0{1}x}".format(self.blue,4)
		game_data += "{0:#0{1}x}".format(self.green,4)
		for i in self.game_matrix:
			game_data += str(i)
		return game_data

	def init_curses(self):
		self.stdscr = curses.initscr()
		curses.noecho()
		curses.cbreak()
		self.stdscr.keypad(1)
		self.n_win = curses.newwin(50, 50, 0, 0)

	def end_curses(self):
		curses.nocbreak()
		self.stdscr.keypad(0)
		curses.echo()
		curses.endwin()

def main():

	controller = Controller(16, 16)
	m_game = controller.init_mat()

	controller.init_curses()

	disp_opt = controller.DISPLAY_ALL
	if len(sys.argv) > 1:
		if sys.argv[1] == "--tl":
			disp_opt = controller.DISPLAY_TL
		if sys.argv[1] == "--tr":
			disp_opt = controller.DISPLAY_TR
		if sys.argv[1] == "--bl":
			disp_opt = controller.DISPLAY_BL
		if sys.argv[1] == "--br":
			disp_opt = controller.DISPLAY_BR
	controller.set_display_mode(disp_opt)

	while(True):
		m_game = controller.calc_grid(m_game)
		controller.set_game_matrix(m_game)
		controller.draw_grid(n_win, controller.get_partial_grid(m_game))
		time.sleep(0.1)

	controller.end_curses()

if __name__ == '__main__':
	main()
