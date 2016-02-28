#!/usr/bin/env python

import time

import _rpi_ws281x as ws


class Led:
	def __init__(self):
		
		# LED configuration
		self.LED_CHANNEL 	= 0  	
		self.LED_COUNT 		= 16 		# LEDs to light
		self.LED_FREQ_HZ 	= 800000 	# Frequency of LED signal (800khz | 400khz)
		self.LED_DMA_NUM 	= 5 		# DMA channel to use (0 - 14)
		self.LED_GPIO 		= 18 		# Pin connected to the signal line (PWM)
		self.LED_BRIGHTNESS 	= 255 		# 0 is dark, 255 is hella bright nigga
		self.LED_INVERT 		= 0 		# 1 inverts LED signal

		# Define colors to be used (unsigned 32-bit int value
		self.DOT_COLORS = [
			0x100010 	# purple
		]

		# Create struct from LED configuration
		self.leds = ws.new_ws2811_t()

		# Init all channels to off
		for channum in range(2):
			channel = ws.ws2811_channel_get(self.leds, channum)
			ws.ws2811_channel_t_count_set(channel, 0)
			ws.ws2811_channel_t_gpionum_set(channel, 0)
			ws.ws2811_channel_t_invert_set(channel, 0)
			ws.ws2811_channel_t_brightness_set(channel, 0)


		channel = ws.ws2811_channel_get(self.leds, self.LED_CHANNEL)

		ws.ws2811_channel_t_count_set(channel, self.LED_COUNT)
		ws.ws2811_channel_t_gpionum_set(channel, self.LED_GPIO)
		ws.ws2811_channel_t_invert_set(channel, self.LED_INVERT)
		ws.ws2811_channel_t_brightness_set(channel, self.LED_BRIGHTNESS)

		ws.ws2811_t_freq_set(self.leds, self.LED_FREQ_HZ)
		ws.ws2811_t_dmanum_set(self.leds, self.LED_DMA_NUM)

		# Initialize library with LED configuration.
		self.resp = ws.ws2811_init(self.leds)
		if self.resp != 0:
			raise RuntimeError('ws2811_init failed with code {0}'.format(self.resp))

	def do_light(self):

		# Wrap following code in a try/finally to ensure cleanup functions are called
		# after library is initialized.
		try:
			offset = 0
			while True:
				color = self.DOT_COLORS[0]
				# Set the LED color buffer value.
				ws.ws2811_led_set(channel, 0, color)

				# Send the LED color data to the hardware.
				self.resp = ws.ws2811_render(self.leds)
				if self.resp != 0:
					raise RuntimeError('ws2811_render failed with code {0}'.format(self.resp))

				# Delay for a small period of time.
				time.sleep(0.25)

		finally:
			# Ensure ws2811_fini is called before the program quits.
			ws.ws2811_fini(self.leds)
			# Example of calling delete function to clean up structure memory.  Isn't
			# strictly necessary at the end of the program execution here, but is good practice.
			ws.delete_ws2811_t(self.leds)

led_c = Led()
led_c.do_light()
