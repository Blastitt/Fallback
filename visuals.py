#!/usr/bin/env python2

class Lights():

	def __init__(self, quadrant_mapping, color):

		self.quadrant_mapping_file = open(quadrant_mapping, 'r')
		self.color = color

	def update(self, partial_light_array):

		# partial_light_array contains integer 1 or 0 (on/off) for each LED.
		# LEDs are represented in READING ORDER (Top Left to Bottom Right).

	def change_color(self, color):

		# color is an INT representing a color (you choose which int corresponds to which color)