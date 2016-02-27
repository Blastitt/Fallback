#!/usr/bin/env python2

import socket
import time
import ws2812

class Client():

	def __init__(self, server):

		self.server = server
		self.connection = None

		self.data = None

	def connect(self):
		try:
			self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.connection.connect(self.server)
			return 1
		except Exception as e:
			print("[!] Error connecting to server: " + str(e))
			raise e

	def send(self, message):
		try:
			self.connection.sendall(message)
		except Exception as e:
			print("[!] Error sending to server: " + str(e))

	def recv(self):
		try:
			self.data = self.connection.recv(2048)
		except Exception as e:
			print("[!] Error receiving data from server: " + str(e))

	def getdata(self):

		return self.data

	def process(self):
		#Process and send new board layout to LEDs
		return 0

	def close(self):
		self.connection.close()
		return 0

def main():

	client = Client(('0.0.0.0', 8000))

	while(True):
		# Connect to server, send request for updated board,
		# receive updated board, process and send data to LEDs,
		# close connection. Repeat @ 10Hz.
		client.connect()
		client.send("heartbeat")
		client.recv()
		data = client.getdata()
		if(data):
			print(data)
		client.close()
		time.sleep(0.1)

if __name__ == '__main__':
	main()